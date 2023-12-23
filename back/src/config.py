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


PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_HOST = os.environ["PG_HOST"]
PG_PORT = int(os.environ["PG_PORT"])
PG_DB = os.environ["PG_DB"]

FILEID_LEN = int(os.getenv("FILEID_LEN", "10"))
FILE_MAXSIZE = int(os.environ["FILE_MAXSIZE"])
FILE_MAXSIZE_IN_BYTES = int(os.environ["FILE_MAXSIZE"]) * 1024**2
