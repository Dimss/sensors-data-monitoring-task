import socket
import os
import random
from threading import Thread
from loguru import logger as log


class MetricsSimulator(Thread):

    def __init__(self, socket_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_path = socket_path
        self.should_terminated = False
        self.init_unix_socket_path()
        self.server = self.init_server_socket()

    def init_unix_socket_path(self) -> None:
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

    def init_server_socket(self) -> socket:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen()
        return server

    def run(self) -> None:
        while not self.should_terminated:
            conn, addr = self.server.accept()
            conn.send(random.randint(-100, 2000).to_bytes(2, 'big', signed=True))
            conn.close()
        log.info("simulator terminated")

    def terminate(self) -> None:
        log.info("terminating metrics simulator...")
        self.should_terminated = True
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(self.socket_path)
            client.recv(1024)
            client.close()
