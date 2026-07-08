# app/exceptions/handlers.py
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.responses.api_response import ApiResponse


def register_exception_handlers(app: FastAPI):
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response_body.model_dump(),
        )
