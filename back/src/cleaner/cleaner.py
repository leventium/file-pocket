from datetime import timedelta
from time import sleep

from sqlmodel import Session
from config import logger, EXPIRE_TIME, CLEANUP_PERIOD
from web.crud import FileCRUD
from web.database import engine


def main():
    sleep(10)
    logger.info("Starting file pruning service.")
    with Session(engine) as session:
        crud = FileCRUD(session)
        while True:
            logger.info("Starting cleanup of expired files.")
            crud.delete_expired(timedelta(hours=EXPIRE_TIME))
            sleep(CLEANUP_PERIOD * 60 * 60)
