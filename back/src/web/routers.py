import os
from asyncio import sleep

from fastapi import APIRouter, Depends
from prepare import logger

from .crud import FileCRUD
from .dependencies import get_file, get_file_crud
from .models import RWFile
from . import responses as resp

file_router = APIRouter(prefix="/api/v1/file_service")


FILE_MAXSIZE_IN_BYTES = int(os.environ["FILE_MAXSIZE"]) * 1024**2


@file_router.post("/file")
async def put_file(
    file: RWFile = Depends(get_file), crud: FileCRUD = Depends(get_file_crud)
):
    logger.info("POST /file")
    if len(file.blob) > FILE_MAXSIZE_IN_BYTES:
        logger.info(
            f"File too large: {file.blob}B resieved. "
            f"{FILE_MAXSIZE_IN_BYTES}B - maximum. Aborting..."
        )
        return resp.FILE_TOO_LARGE
    logger.info("Saving file to DB...")
    crud.save_file(file)
    return resp.CREATED


@file_router.get("/file")
async def recieve_file(file_id: str, crud: FileCRUD = Depends(get_file_crud)):
    await sleep(5)
    logger.info(f"GET /file?file_id={file_id}")
    logger.info("Fetching file from DB...")
    res = crud.get_file_by_id(file_id)
    if res is None:
        logger.info(f"'{file_id}' not found...")
        return resp.FILE_NOT_FOUND
    logger.info(f"Sending '{file_id}' to user...")
    return resp.get_file_responce(res.blob, res.filename)
