import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.config.logger import logger
from app.utils.logger import parse_request_body


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        body = await request.body()

        async def receive():
            return {
                "type": "http.request",
                "body": body,
                "more_body": False,
            }
        
        request._receive = receive

        payload = parse_request_body(body)

        response = await call_next(request)

        duration = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            payload=payload,
            agent=request.headers.get("User-Agent"),
            ip_address=request.client.host,
            status=response.status_code,
            duration_ms=duration,
        )

        return response
