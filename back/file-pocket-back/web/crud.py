from datetime import datetime, timedelta
from random import choice
from typing import Optional

from models import File, RWFile
from prepare import logger
from sqlalchemy.engine import Engine
from sqlmodel import Session, func, select

ID_SYMBOLS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"


class FileCRUD:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def _create_id(self) -> str:
        res = ""
        id_ok = False
        while not id_ok:
            res = ""
            for _ in range(10):
                res += choice(ID_SYMBOLS)
            with Session(self.engine) as session:
                id_exists = session.exec(
                    select(func.count("*"))
                    .select_from(File)
                    .where(File.id == res)
                ).first()
            if id_exists == 0:
                id_ok = True
        return res

    def save_file(self, file: RWFile):
        db_file = File.model_validate(file)
        db_file.id = self._create_id()
        db_file.created_at = datetime.now()
        with Session(self.engine) as session:
            logger.info(f"'{db_file.id}' saved.")
            session.add(file)
            session.commit()

    def get_file_by_id(self, id: str) -> Optional[File]:
        with Session(self.engine) as session:
            res = session.exec(select(File).where(File.id == id)).first()
            if res is not None:
                logger.info(f"'{id}' saved.")
                session.delete(res)
                session.commit()
            return res

    def delete_expired(self, exp_time: timedelta):
        with Session(self.engine) as session:
            exp_files = session.exec(
                select(File)
                .where(File.created_at + exp_time > datetime.now())
            ).all()
            for file in exp_files:
                logger.info(f"Deleting file '{file.id}'.")
                session.delete(file)
            session.commit()
