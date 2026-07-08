from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.router import router
from app.config.database import engine
from app.config.logger import logger
from app.config.settings import settings
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
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.include_router(router)
