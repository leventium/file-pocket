import os
from contextlib import asynccontextmanager
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI

from prepare import logger
from web.database import engine, init_schema
from web.routers import file_router
import cleaner


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the server.")
    init_schema(engine)
    yield
    logger.info("Stopping the server.")


app = FastAPI(lifespan=lifespan)
app.include_router(file_router)


if __name__ == "__main__":
    Process(target=cleaner.main).start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
