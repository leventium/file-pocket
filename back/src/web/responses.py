from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def get_file_response(file: bytes, filename: str) -> Response:
    return Response(
        content=file,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        },
        media_type="application/octet-stream",
        status_code=status.HTTP_200_OK,
    )


class CreatedResponse(BaseModel):
    file_id: str


def get_success_response(file_id: str):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CreatedResponse(file_id=file_id).model_dump(),
    )
