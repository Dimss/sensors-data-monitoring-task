import asyncio
from threading import Thread
from queue_impl import redis_queue as q
from loguru import logger as log
from config import config


class Alerter(Thread):
    def __init__(self, cfg: config.Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shutdown = False
        self.queue = q.RedisQueue(cfg.queue.redis)
        self.message_generator = self.queue.listen()
        self.listen_and_process_task = None

    def shutdown(self):
        self._shutdown = True

    async def _listen_and_process(self):
        async for message in self.queue.listen():
            log.info(message)

    async def _subscribe(self):
        self.listen_and_process_task = asyncio.create_task(self._listen_and_process())
        await self.listen_and_process_task

    def run(self):
        asyncio.run(self._subscribe())

    def stop(self):
        if self.listen_and_process_task is not None:
            self.listen_and_process_task.cancel()


class SlackAlerter:
    pass
