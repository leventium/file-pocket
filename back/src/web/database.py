import os

from sqlalchemy import URL
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine
from prepare import logger

from . import models  # noqa: F401

logger.debug("Creating database engine.")
engine = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
        host=os.environ["PG_HOST"],
        port=int(os.environ["PG_PORT"]),
        database=os.environ["PG_DB"],
    )
)


def init_schema(engine: Engine):
    logger.debug("Creating database schema.")
    SQLModel.metadata.create_all(engine)
