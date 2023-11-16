import socket
import asyncio
from loguru import logger as log


class BaseSensor:
    def __init__(self, sensor_name: str, socket_path: str):
        self.sensor_name = sensor_name
        self.socket_path = socket_path
        pass

    def read_metrics(self) -> int:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(self.socket_path)
            metric = client.recv(1024)
            client.close()
            return int.from_bytes(metric, byteorder='big', signed=True)

    def get_sensor_name(self) -> str:
        return self.sensor_name


class TemperatureSensor(BaseSensor):
    def __init__(self, socket_path: str):
        super().__init__(self.__class__.__name__, socket_path)
        self._shutdown = False

    async def read_metrics(self) -> int:
        while not self.is_shutdown():
            log.info(f"in read metric {self.get_sensor_name()}")
            await asyncio.sleep(1)
            yield super().read_metrics()
        log.info(f"shutting down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()

    def is_shutdown(self):
        return self._shutdown

    def shutdown(self):
        log.info("shutdown TemperatureSensor")
        self._shutdown = True


class HumiditySensor(BaseSensor):
    def __init__(self, socket_path: str):
        super().__init__(self.__class__.__name__, socket_path)
        self._shutdown = False

    async def read_metrics(self) -> int:
        while not self._shutdown:
            await asyncio.sleep(1)
            yield super().read_metrics()
        log.info(f"shutting down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()

    def shutdown(self):
        self._shutdown = True


class PressureSensor(BaseSensor):
    def __init__(self, socket_path: str):
        super().__init__(self.__class__.__name__, socket_path)
        self._shutdown = False

    async def read_metrics(self) -> int:
        while not self._shutdown:
            await asyncio.sleep(1)
            yield super().read_metrics()
        log.info(f"shutting down {self.get_sensor_name()}")

    def get_sensor_name(self) -> str:
        return super().get_sensor_name()

    def shutdown(self):
        self._shutdown = True
