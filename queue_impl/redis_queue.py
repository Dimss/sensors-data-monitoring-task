import asyncio
import time

from loguru import logger as log
import redis
from config import config


class RedisQueue:
    def __init__(self, cfg: config.RedisQueue):
        self.cfg = cfg
        self.pubsub = None
        self.redis = None
        self.set_redis_connection()

    def set_redis_connection(self):
        self.redis = redis.Redis(host=self.cfg.host, port=self.cfg.port, decode_responses=True, health_check_interval=1)
        while not self.conn_ok():
            log.warning("error connecting to redis, retrying in 1 sec...")
            time.sleep(1)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)

    def conn_ok(self) -> bool:
        try:
            self.redis.ping()
        except redis.ConnectionError:
            return False
        return True

    async def listen(self):
        self.pubsub.subscribe(self.cfg.channel)
        try:
            while True:
                await asyncio.sleep(0.1)
                try:
                    message = self.pubsub.get_message()
                    if message:
                        yield message
                except redis.ConnectionError:
                    self.set_redis_connection()
                    self.pubsub.subscribe(self.cfg.channel)
        except asyncio.CancelledError:
            log.info("shutdown redis queue")

    def publish(self, msg: str):
        try:
            self.redis.publish(self.cfg.channel, msg)
        except redis.ConnectionError:
            self.set_redis_connection()
            self.publish(msg)
