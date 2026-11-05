"""Application errors and the handlers that turn every failure into ``{code, message, details}``."""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("exampro")


class AppError(Exception):
    """Base class for expected, client-facing errors."""

    status_code: int = 400
    code: str = "BAD_REQUEST"

    def __init__(self, message: str, *, code: str | None = None, status_code: int | None = None,
                 details: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.details = details


class BadRequestError(AppError):
    status_code, code = 400, "BAD_REQUEST"


class UnauthorizedError(AppError):
    status_code, code = 401, "UNAUTHORIZED"


class ForbiddenError(AppError):
    status_code, code = 403, "FORBIDDEN"


class NotFoundError(AppError):
    status_code, code = 404, "NOT_FOUND"


class ConflictError(AppError):
    status_code, code = 409, "CONFLICT"


class UnprocessableError(AppError):
    status_code, code = 422, "UNPROCESSABLE"


def error_body(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "details": details}


def register_exception_handlers(app: FastAPI) -> None:
    """Attach handlers so all errors share one JSON shape."""

    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
        return JSONResponse(status_code=exc.status_code, headers=headers,
                            content=jsonable_encoder(error_body(exc.code, exc.message, exc.details)))

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content=jsonable_encoder(
            error_body("VALIDATION_ERROR", "Request validation failed", exc.errors())))

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = {401: "UNAUTHORIZED", 403: "FORBIDDEN", 404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}.get(
            exc.status_code, "HTTP_ERROR")
        return JSONResponse(status_code=exc.status_code, headers=getattr(exc, "headers", None),
                            content=error_body(code, str(exc.detail), None))

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(status_code=500, content=error_body("INTERNAL_ERROR", str(exc) or "Something went wrong.", repr(exc)))
