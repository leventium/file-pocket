from dotenv import load_dotenv
from loguru import logger


load_dotenv()
logger.add("logs/info.log", level="INFO", rotation="10 MB")
logger.add("logs/error.log", level="ERROR", rotation="10 MB")
