import os

from sqlalchemy import URL
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine

from . import models  # noqa: F401

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
    SQLModel.metadata.create_all(engine)
