from fastapi import FastAPI, Request, status
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
)
from fastapi.responses import JSONResponse

from app.responses.api_response import ApiResponse


def register_exception_handlers(app: FastAPI):
    # --- Handler Eksisting untuk Validasi Skema (Selalu 422) ---
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = exc.errors()
        error_messages = []
        parsed_errors = []

        for err in errors:
            loc = ".".join(str(x) for x in err["loc"])
            msg = err["msg"]
            type_error = err["type"]

            error_messages.append(f"[{loc}]: {msg}")
            parsed_errors.append({"field": loc, "issue": msg, "type": type_error})

        combined_message = "Validation failed: " + ", ".join(error_messages)

        response_body = ApiResponse[list](
            success=False,
            message=combined_message,
            data=parsed_errors,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_body.model_dump(),
        )

    # --- Handler Baru untuk Error Dinamis (400, 404, 409, dll) ---
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        response_body = ApiResponse[None](
            success=False,
            message=str(exc.detail),
            data=None,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response_body.model_dump(),
        )
