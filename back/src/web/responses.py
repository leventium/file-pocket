from fastapi import Response, status
from fastapi.responses import JSONResponse

from config import FILE_MAXSIZE

def get_file_responce(file: bytes, filename: str) -> Response:
    return Response(
        content=file,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        },
        media_type="application/octet-stream",
        status_code=status.HTTP_200_OK,
    )

CREATED = Response(
    status_code=status.HTTP_201_CREATED,
)

FILE_NOT_FOUND = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"error": {"message": "file not found."}},
)

FILE_TOO_LARGE = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content={
        "error": {
            "message": "file too large.",
            "file_maxsize": FILE_MAXSIZE,
        }
    },
)
