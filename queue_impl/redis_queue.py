import asyncio
from loguru import logger as log
import redis
from config import config


class RedisQueue:
    def __init__(self, cfg: config.RedisQueue):
        self.channel = cfg.channel
        self.redis = redis.Redis(host=cfg.host, port=cfg.port, decode_responses=True)
        self.p = self.redis.pubsub(ignore_subscribe_messages=False)

    def subscribe(self):
        self.p.subscribe(self.channel)

    async def listen(self):
        try:
            while True:
                await asyncio.sleep(0.1)
                message = self.p.get_message()
                if message:
                    yield message
        except asyncio.CancelledError as e:
            pass
        finally:
            log.info("shutdown redis queue")

    def publish(self, msg: str):
        self.redis.publish(self.channel, msg)
