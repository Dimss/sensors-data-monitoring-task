import yaml
from pathlib import Path
from pydantic import BaseModel
from os import environ

CONFIG_FILE_NAME = "config.yml"
CONFIG_FILE_PATH = Path(__file__).with_name(CONFIG_FILE_NAME)


class SlackConfig(BaseModel):
    channel: str
    token: str


class Alerts(BaseModel):
    slack: SlackConfig


class RedisQueue(BaseModel):
    host: str
    port: int
    channel: str


class Queue(BaseModel):
    redis: RedisQueue


class SensorValidRange(BaseModel):
    min: int
    max: int


class SensorConfig(BaseModel):
    name: str
    enabled: bool
    validRange: SensorValidRange


class Config(BaseModel):
    sensors: list[SensorConfig]
    queue: Queue
    alerts: Alerts


def load_config() -> Config:
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = yaml.safe_load(file)
        return _override_with_env_var(Config(**config))


def _override_with_env_var(cfg: Config) -> Config:
    if environ.get('REDIS_HOST') is not None:
        cfg.queue.redis.host = environ.get('REDIS_HOST')

    if environ.get('SLACK_TOKEN') is not None:
        cfg.alerts.slack.token = environ.get('SLACK_TOKEN')

    if environ.get('SLACK_CHANNEL') is not None:
        cfg.alerts.slack.channel = environ.get('SLACK_CHANNEL')

    return cfg
