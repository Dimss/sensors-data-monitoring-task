import yaml
from pathlib import Path
from pydantic import BaseModel

CONFIG_FILE_NAME = "config.yml"
CONFIG_FILE_PATH = Path(__file__).with_name(CONFIG_FILE_NAME)


class SensorValidRange(BaseModel):
    min: int
    max: int


class SensorConfig(BaseModel):
    name: str
    enabled: bool
    validRange: SensorValidRange


class Config(BaseModel):
    sensors: list[SensorConfig]


def load_config() -> Config:
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = yaml.safe_load(file)
        return Config(**config)
