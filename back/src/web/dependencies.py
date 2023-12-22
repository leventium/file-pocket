from fastapi import UploadFile
from sqlmodel import Session

from .crud import FileCRUD
from .database import engine
from .models import RWFile


async def get_file(file: UploadFile):
    blob = await file.read()
    return RWFile(
        filename=file.filename if file.filename is not None else "file",
        blob=blob,
    )


async def get_file_crud():
    with Session(engine) as sess:
        yield FileCRUD(sess)
