from sqlalchemy import URL
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine
from config import logger, PG_USER, PG_PASSWORD, PG_HOST, PG_DB, PG_PORT

from . import models  # noqa: F401

logger.debug("Creating database engine.")
engine = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
    )
)


def init_schema(engine: Engine):
    logger.debug("Creating database schema.")
    SQLModel.metadata.create_all(engine)
