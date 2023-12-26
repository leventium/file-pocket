from fastapi import status, Request, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import FILE_MAXSIZE


class TooLargeFileError(Exception):
    def __init__(self, file_size: int) -> None:
        self.file_size = file_size


class TooLargeResponse(BaseModel):
    message: str
    file_maxsize: int
    recieved_size: int


async def handle_too_large_file(req: Request, exc: TooLargeFileError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=TooLargeResponse(
            message="File too large.",
            file_maxsize=FILE_MAXSIZE,
            recieved_size=exc.file_size // 1024**2,
        ).model_dump(),
    )


class NotFoundError(Exception):
    pass


class Message(BaseModel):
    message: str


async def handle_not_found(req: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Message(message="File not found.").model_dump(),
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(TooLargeFileError, handle_too_large_file)
    app.add_exception_handler(NotFoundError, handle_not_found)
