from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.router import router
from app.config.database import engine
from app.config.settings import settings
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 {settings.APP_NAME} started")

    yield

    await engine.dispose()

    print("🛑 Application stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.include_router(router)
