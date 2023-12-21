import sys
from datetime import timedelta
from signal import SIGTERM, signal
from time import sleep

from prepare import logger
from sqlalchemy.engine import Engine
from web.crud import FileCRUD


def main(engine: Engine):
    logger.info("Starting file prunign service.")
    signal(SIGTERM, lambda num, frame: sys.exit())
    crud = FileCRUD(engine)
    while True:
        logger.info("Start daily check.")
        crud.delete_expired(timedelta(days=1))
        sleep(24 * 60 * 60)
