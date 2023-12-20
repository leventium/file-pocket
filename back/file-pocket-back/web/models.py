from datetime import datetime
from sqlmodel import SQLModel, Field


class File(SQLModel, table=True):
    id: str = Field(primary_key=True)
    filename: str
    blob: bytes
    created_at: datetime


class RWFile(SQLModel):
    filename: str
    blob: bytes
