import sys
from datetime import timedelta
from signal import SIGTERM, signal
from time import sleep

from sqlmodel import Session
from config import logger
from web.crud import FileCRUD
from web.database import engine


def main():
    logger.info("Starting file pruning service.")
    signal(SIGTERM, lambda num, frame: sys.exit())
    with Session(engine) as session:
        crud = FileCRUD(session)
        while True:
            logger.info("Start daily check.")
            crud.delete_expired(timedelta(days=1))
            sleep(24 * 60 * 60)
