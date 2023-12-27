import os
import sys
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


_LOG_LEVEL = "DEBUG" if "DEBUG" in os.environ else "INFO"
logger.remove()
logger.add(sys.stderr, level=_LOG_LEVEL)
logger.add("logs/info.log", level=_LOG_LEVEL, rotation="10 MB")
logger.add("logs/error.log", level="ERROR", rotation="10 MB")


PROXY_PATH = os.getenv("PROXY_PATH", "")

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "postgres")

FILEID_LEN = int(os.getenv("FILEID_LEN", "10"))
FILE_MAXSIZE = (
    int(os.getenv("FILE_MAXSIZE", "100"))
    if "DEBUG" not in os.environ
    else 2
)
FILE_MAXSIZE_IN_BYTES = FILE_MAXSIZE * 1024**2
