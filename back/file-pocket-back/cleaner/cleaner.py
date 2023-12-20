from time import sleep
from datetime import timedelta
import sys
from prepare import logger
from signal import signal, SIGTERM
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
