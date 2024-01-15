from contextlib import asynccontextmanager
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import logger, PROXY_PATH, PORT, DEBUG_MODE
from metadata import description, tags
from web.database import engine, init_schema
from web.routers import file_router
from web.exceptions import register_exceptions
import cleaner


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the server.")
    init_schema(engine)
    yield
    logger.info("Stopping the server.")


app = FastAPI(
    lifespan=lifespan,
    root_path=PROXY_PATH,
    title="File Pocket",
    description=description,
    openapi_tags=tags,
    version="0.1.0",
)
app.include_router(file_router)
register_exceptions(app)


if DEBUG_MODE:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )


if __name__ == "__main__":
    Process(target=cleaner.main).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
