import socket
import asyncio
from loguru import logger as log
from config import config


class BaseSensor:
    def __init__(self, sensor_name: str, socket_path: str, cfg: config.SensorConfig):
        self.sensor_name = sensor_name
        self.socket_path = socket_path
        self.cfg = cfg

    def read_metrics(self) -> int:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(self.socket_path)
            metric = client.recv(1024)
            client.close()
            return int.from_bytes(metric, byteorder='big', signed=True)

    def get_sensor_name(self) -> str:
        return self.sensor_name


class TemperatureSensor(BaseSensor):
    def __init__(self, socket_path: str, cfg: config.SensorConfig):
        super().__init__(self.__class__.__name__, socket_path, cfg)

    async def read_metrics(self) -> int:
        try:
            while True:
                await asyncio.sleep(1)
                yield super().read_metrics()
        except asyncio.CancelledError as e:
            pass
        finally:
            log.info(f"shutdown down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()


class HumiditySensor(BaseSensor):
    def __init__(self, socket_path: str, cfg: config.SensorConfig):
        super().__init__(self.__class__.__name__, socket_path, cfg)

    async def read_metrics(self) -> int:
        try:
            while True:
                await asyncio.sleep(1)
                yield super().read_metrics()
        except asyncio.CancelledError as e:
            pass
        finally:
            log.info(f"shutdown down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()


class PressureSensor(BaseSensor):
    def __init__(self, socket_path: str, cfg: config.SensorConfig):
        super().__init__(self.__class__.__name__, socket_path, cfg)

    async def read_metrics(self) -> int:
        try:
            while True:
                await asyncio.sleep(1)
                yield super().read_metrics()
        except asyncio.CancelledError as e:
            pass
        finally:
            log.info(f"shutdown down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()
