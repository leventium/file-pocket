from crud import FileCRUD
from database import engine
from fastapi import UploadFile
from models import RWFile


async def get_file(file: UploadFile) -> RWFile:
    blob = await file.read()
    return RWFile(
        filename=file.filename if file.filename is not None else "file",
        blob=blob,
    )


async def get_file_crud() -> FileCRUD:
    return FileCRUD(engine)
