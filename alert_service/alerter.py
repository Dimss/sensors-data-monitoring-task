import asyncio
import requests
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
        self.slack_alerter = SlackAlerter(cfg.alerts.slack.channel, cfg.alerts.slack.token)

    def shutdown(self):
        self._shutdown = True

    async def _listen_and_process(self):
        async for message in self.queue.listen():
            # event_data = json.loads(message)
            log.info(message['data'])
            self.slack_alerter.post_message(message['data'])

    async def _subscribe(self):
        self.listen_and_process_task = asyncio.create_task(self._listen_and_process())
        await self.listen_and_process_task

    def run(self):
        asyncio.run(self._subscribe())

    def stop(self):
        if self.listen_and_process_task is not None:
            self.listen_and_process_task.cancel()


class SlackAlerter:
    def __init__(self, channel_id: str, token: str):
        self.channel_id = channel_id
        self.token = token
        self.message_endpoint = "https://slack.com/api/chat.postMessage"

    def post_message(self, message: str):
        payload = {'channel': self.channel_id, 'text': message}
        headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
        res = requests.post(self.message_endpoint, headers=headers, json=payload).json()
        if not res['ok']:
            log.warning("failed to deliver alert to slack channel")
