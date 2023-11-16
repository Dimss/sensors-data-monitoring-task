import click
from loguru import logger as log
from main_service import orchestrator as o

from signal import SIGINT, SIGTERM, sigwait
from config import config


@click.command()
def sensor_connectors():
    orchestrator = o.MainOrchestrator(config.load_config())
    orchestrator.start()
    sigwait({SIGINT, SIGTERM})
    log.info("exiting...")
    orchestrator.stop()
    orchestrator.join()
    log.info("bye bye")


@click.group()
def start():
    pass


@click.group()
def cli():
    pass


start.add_command(sensor_connectors)
cli.add_command(start)

if __name__ == '__main__':
    cli()
