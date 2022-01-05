import logging
import time
from datetime import datetime

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI, Header, Request
from src.config import settings
from src.presentation.controller.example import router as example_router
from src.presentation.controller.member import router as member_router
from src.presentation.controller.project import router as project_router

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


async def verify_token(x_token: str = Header(...)):  # noqa
    pass

space = "  "

app = FastAPI(
    debug=True,
    title="api title",
    description=f"""
api{space}
description{space}
[リンクサンプル](https://google.com){space}
    """,
    version="0.0.1",
    root_path="",
    dependencies=[Depends(verify_token)])
app.include_router(project_router)
app.include_router(member_router)
app.include_router(example_router)


@app.on_event("startup")
async def startup():  # noqa
    logger.debug("startup")


@app.on_event("shutdown")
async def shutdown():  # noqa
    logger.debug("shutdown")


@app.middleware("http")
async def process_time(request: Request, call_next):  # noqa
    path = request.url.path
    method = request.method
    start = time.perf_counter()
    start_datetime = datetime.now().isoformat()

    logger.debug(f"{start_datetime} {method} {path}: start")

    response = await call_next(request)

    end = time.perf_counter()
    end_datetime = datetime.now().isoformat()
    logger.debug(f"{end_datetime} {method} {path}: {end - start}")

    return response


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=False)
