import sys
from datetime import timedelta
from signal import SIGTERM, signal
from time import sleep

from sqlmodel import Session
from config import logger, EXPIRE_TIME, CLEANUP_PERIOD
from web.crud import FileCRUD
from web.database import engine


def main():
    logger.info("Starting file pruning service.")
    signal(SIGTERM, lambda num, frame: sys.exit())
    with Session(engine) as session:
        crud = FileCRUD(session)
        while True:
            logger.info("Starting cleanup of expired files.")
            crud.delete_expired(timedelta(hours=EXPIRE_TIME))
            sleep(CLEANUP_PERIOD * 60 * 60)
