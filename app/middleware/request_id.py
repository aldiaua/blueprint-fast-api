import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from app.context.request_context import request_id_ctx

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID")

        if request_id is None:
            request_id = str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        request_id_ctx.set(request_id)
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response
