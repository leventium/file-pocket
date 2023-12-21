import os
from multiprocessing import Process

import cleaner
import uvicorn
from fastapi import FastAPI
from prepare import logger
from web.database import engine, init_schema
from web.routers import file_router

app = FastAPI()
app.include_router(file_router)


@app.on_event("startup")
async def on_startup():
    logger.info("Starting the server.")
    init_schema(engine)


if __name__ == "__main__":
    Process(target=cleaner.main, args=(engine,))
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
