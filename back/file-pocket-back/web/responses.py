import os

from fastapi import Response, status

CREATED = Response(
    status_code=status.HTTP_201_CREATED,
)

FILE_NOT_FOUND = Response(
    status_code=status.HTTP_404_NOT_FOUND,
    media_type="application/json",
    content={"error": "file not found."}
)

FILE_TOO_LARGE = Response(
    status_code=status.HTTP_400_BAD_REQUEST,
    media_type="application/json",
    content={
        "error": "file too large.",
        "file_maxsize": int(os.environ["FILE_MAXSIZE"]),
    }
)
