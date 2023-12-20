from asyncio import sleep
import os
from fastapi import APIRouter, Depends
from prepare import logger
from dependencies import get_file, get_file_crud
from crud import FileCRUD
from models import RWFile
from responses import CREATED, FILE_NOT_FOUND, FILE_TOO_LARGE


file_router = APIRouter(prefix="/api/v1/file_service")


FILE_MAXSIZE_IN_BYTES = int(os.environ["FILE_MAXSIZE"]) * 1024**2


@file_router.post("/file")
async def put_file(
    file: RWFile = Depends(get_file),
    crud: FileCRUD = Depends(get_file_crud)
):
    if len(file.blob) > FILE_MAXSIZE_IN_BYTES:
        return FILE_TOO_LARGE
    crud.save_file(file)
    return CREATED


@file_router.get("/file")
async def recieve_file(
    file_id: str,
    crud: FileCRUD = Depends(get_file_crud)
):
    await sleep(5)
    res = crud.get_file_by_id(file_id)
    if res is None:
        return FILE_NOT_FOUND
    return RWFile.model_validate(res)
