import click
from loguru import logger as log
from main_service import orchestrator as o
from alert_service import alerter as a
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


@click.command()
def alerter():
    alert_mgr = a.Alerter(config.load_config())
    alert_mgr.start()
    sigwait({SIGINT, SIGTERM})
    log.info("exiting...")
    alert_mgr.stop()
    alert_mgr.join()
    log.info("bye bye")


@click.group()
def start():
    pass


@click.group()
def cli():
    pass


start.add_command(sensor_connectors)
start.add_command(alerter)

cli.add_command(start)

if __name__ == '__main__':
    cli()
