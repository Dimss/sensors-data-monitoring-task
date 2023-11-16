import asyncio
import time
import random
from threading import Thread
from loguru import logger as log
from config import config
from sensors import sensors, simulator
import importlib


class MainOrchestrator(Thread):

    def __init__(self, cfg: config.Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = cfg
        self._terminate = False
        self._metric_simulator_socket_path = "/tmp/metric-simulator.sock"
        self._metric_simulator = self._get_metric_simulator()
        self._sensors_instances = []

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
        for sensor in self.cfg.sensors:
            if sensor.enabled:
                self._sensors_instances.append(
                    # create sensor instance based on the configuration
                    getattr(
                        importlib.import_module("sensors.sensors"),
                        sensor.name
                    )(self._metric_simulator_socket_path)
                )

        await asyncio.gather(*self._compose_async_executors())

    def _compose_async_executors(self) -> []:
        async_executors = []
        for i in self._sensors_instances:
            async_executors.append(self.stream_and_validate(i))
        return async_executors

    async def stream_and_validate(self, sensor_instance):
        log.info(f"starting metric stream for {sensor_instance.get_sensor_name()}")
        async for metric in sensor_instance.read_metrics():
            log.info(f"sensor name: {sensor_instance.get_sensor_name()} value: {metric}")

    def run(self):
        self._start_metric_simulator()
        asyncio.run(self._start_sensors_monitors())
        log.info("orchestrator is done ------------------ ")

    def stop(self):
        self._terminate_metric_simulator()
        for i in self._sensors_instances:
            i.shutdown()
