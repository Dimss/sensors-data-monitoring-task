from loguru import logger as log
from main_service import orchestrator as o

from signal import SIGINT, SIGTERM, sigwait
from config import config


def main():
    orchestrator = o.MainOrchestrator(config.load_config())
    orchestrator.start()
    sigwait({SIGINT, SIGTERM})
    log.info("exiting...")
    orchestrator.stop()
    orchestrator.join()
    log.info("bye bye")


if __name__ == '__main__':
    main()
