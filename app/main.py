from contextlib import asynccontextmanager

from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import router
from app.config.database import engine
from app.config.logger import logger
from app.config.settings import settings
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_started", extra={"app": settings.APP_NAME})

    yield

    await engine.dispose()

    logger.info("application_stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
register_exception_handlers(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.include_router(router)

# Ensure the upload directory exists before mounting
upload_dir = Path(settings.LOCAL_STORAGE_PATH)
upload_dir.mkdir(parents=True, exist_ok=True)

# Mount the 'uploads' directory to serve static files
app.mount(f"/{settings.LOCAL_STORAGE_PATH}", StaticFiles(directory=settings.LOCAL_STORAGE_PATH), name="uploads")
