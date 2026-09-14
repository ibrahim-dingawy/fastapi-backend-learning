import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, videos


logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


app = FastAPI()


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        },
    )


@app.middleware("http")
async def log_request_time(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    )

    logger.info(
        "%s %s completed in %.3f seconds",
        request.method,
        request.url.path,
        process_time,
    )

    return response


app.include_router(auth.router)
app.include_router(videos.router)


@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI"
    }


