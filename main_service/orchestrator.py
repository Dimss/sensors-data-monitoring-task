import asyncio
import json
from threading import Thread
from loguru import logger as log
from config import config
from sensors import simulator
import importlib
from queue_impl import redis_queue as q


class MainOrchestrator(Thread):

    def __init__(self, cfg: config.Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = q.RedisQueue(cfg.queue.redis)
        self.cfg = cfg
        self._terminate = False
        self._metric_simulator_socket_path = "/tmp/metric-simulator.sock"
        self._metric_simulator = self._get_metric_simulator()
        self._async_tasks = []

    def _get_metric_simulator(self) -> simulator.MetricsSimulator:
        return simulator.MetricsSimulator(self._metric_simulator_socket_path)

    def _start_metric_simulator(self):
        log.info("starting metrics simulator...")
        self._metric_simulator.start()
        log.info("metrics simulator started")

    def _terminate_metric_simulator(self):
        self._metric_simulator.terminate()
        self._metric_simulator.join()

    async def _start_sensors_monitors(self):
        log.info("starting sensor metric collectors...")
        for sensor_cfg in self.cfg.sensors:
            # append to tasks list
            # each enabled sensors
            if sensor_cfg.enabled:
                self._async_tasks.append(
                    asyncio.create_task(
                        self.stream_and_validate(
                            # create sensor instance based on the configuration
                            getattr(
                                importlib.import_module("sensors.sensors"),
                                sensor_cfg.name
                            )(self._metric_simulator_socket_path, sensor_cfg)
                        )
                    )
                )
        # start and await for the tasks
        await asyncio.gather(*self._async_tasks)

    async def stream_and_validate(self, sensor_instance):
        log.info(f"starting metric stream for {sensor_instance.get_sensor_name()}")
        # read the metric and in case
        # of range violation issue an alert
        async for metric in sensor_instance.read_metrics():
            if sensor_instance.cfg.validRange.min > metric or metric > sensor_instance.cfg.validRange.max:
                message = {
                    'sensor': sensor_instance.get_sensor_name(),
                    'metric_value': metric,
                    'valid_range': [sensor_instance.cfg.validRange.min, sensor_instance.cfg.validRange.max]
                }
                self.queue.publish(json.dumps(message))
                log.warning(f"{message}, issuing alert")
            else:
                log.info(f"[{sensor_instance.get_sensor_name()}] metric [{metric}] in valid range")

    def run(self):
        # start the metric simulator in separate thread
        self._start_metric_simulator()
        # start the async event loop
        asyncio.run(self._start_sensors_monitors())

    def stop(self):
        self._terminate_metric_simulator()
        for t in self._async_tasks:
            t.cancel()
