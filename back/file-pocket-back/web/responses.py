import os

from fastapi import Response, status
from fastapi.responses import JSONResponse

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
            "file_maxsize": int(os.environ["FILE_MAXSIZE"]),
        }
    },
)
