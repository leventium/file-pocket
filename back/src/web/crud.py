import os
from datetime import datetime, timedelta
from random import choice
from typing import Optional

from prepare import logger
from sqlmodel import Session, func, select

from .models import File, RWFile

ID_SYMBOLS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
FILEID_LEN = int(os.getenv("FILEID_LEN", "10"))


class FileCRUD:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _create_id(self) -> str:
        logger.debug("Starting creation of ID.")
        res = ""
        id_ok = False
        while not id_ok:
            res = ""
            for _ in range(FILEID_LEN):
                res += choice(ID_SYMBOLS)

            id_exists = self.session.exec(
                select(func.count("*")).select_from(File).where(File.id == res)
            ).first()

            if id_exists == 0:
                logger.debug(f"'{res}' created.")
                id_ok = True
            else:
                logger.debug(f"'{res}' already exists, retrying...")
        return res

    def save_file(self, file: RWFile):
        db_file = File(
            id=self._create_id(),
            filename=file.filename,
            blob=file.blob,
            created_at=datetime.now(),
        )
        logger.info(f"'{db_file.id}' saved.")
        self.session.add(db_file)
        self.session.commit()

    def get_file_by_id(self, id: str) -> Optional[File]:
        res = self.session.exec(select(File).where(File.id == id)).first()
        if res is not None:
            logger.info(f"'{id}' found. Giving to user...")
            self.session.delete(res)
            self.session.commit()
        return res

    def delete_expired(self, exp_time: timedelta):
        exp_files = self.session.exec(
            select(File).where(File.created_at + exp_time > datetime.now())
        ).all()
        for file in exp_files:
            logger.info(f"Deleting file '{file.id}'.")
            self.session.delete(file)
        self.session.commit()
