from asyncio import sleep

from fastapi import APIRouter, Depends
from config import logger, FILE_MAXSIZE_IN_BYTES

from .crud import FileCRUD
from .dependencies import get_file, get_file_crud
from .models import RWFile
from . import exceptions as exc
from . import responses as resp

file_router = APIRouter(prefix="/file-service")


@file_router.post(
    "/file",
    status_code=201,
    responses={
        201: {
            "model": resp.CreatedResponse,
            "description": "File succssfully stored, its ID is returned.",
        },
        400: {
            "model": exc.TooLargeResponse,
            "description": "File is too large, maximal acceptable "
            "file size is specified in response.",
        },
    },
    tags=["File Service"],
)
async def put_file(
    file: RWFile = Depends(get_file), crud: FileCRUD = Depends(get_file_crud)
):
    logger.info("POST /file")
    if len(file.blob) > FILE_MAXSIZE_IN_BYTES:
        logger.info(
            f"File too large: {len(file.blob)}B resieved. "
            f"{FILE_MAXSIZE_IN_BYTES}B - maximum. Aborting..."
        )
        raise exc.TooLargeFileError(file_size=len(file.blob))
    logger.info("Saving file to DB...")
    new_id = crud.save_file(file)
    return resp.get_success_response(new_id)


@file_router.get(
    "/file",
    status_code=200,
    responses={
        200: {
            "content": {"application/octet-stream": {}},
            "description": "Return file stored with this ID. "
            "File will be removed after recieving.",
        },
        404: {
            "model": exc.Message,
            "description": "File with specified ID wasn't found.",
        },
    },
    tags=["File Service"],
)
async def recieve_file(file_id: str, crud: FileCRUD = Depends(get_file_crud)):
    await sleep(5)
    logger.info(f"GET /file?file_id={file_id}")
    logger.info("Fetching file from DB...")
    res = crud.get_file_by_id(file_id)
    if res is None:
        logger.info(f"'{file_id}' not found...")
        raise exc.NotFoundError()
    logger.info(f"Sending '{file_id}' to user...")
    return resp.get_file_response(res.blob, res.filename)
