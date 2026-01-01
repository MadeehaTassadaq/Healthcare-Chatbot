"""
Error handlers and exception handling middleware.
"""
from typing import Union, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, error_code: str = "app_error", status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(AppException):
    """Authentication-related error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="authentication_error",
            status_code=401,
        )


class AuthorizationError(AppException):
    """Authorization-related error."""

    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(
            message=message,
            error_code="authorization_error",
            status_code=403,
        )


class NotFoundError(AppException):
    """Resource not found error."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            error_code="not_found",
            status_code=404,
        )


class ConflictError(AppException):
    """Resource conflict error."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            error_code="conflict",
            status_code=409,
        )


class ValidationAppError(AppException):
    """Business logic validation error."""

    def __init__(self, message: str, field: str = None):
        error_code = "validation_error"
        if field:
            error_code = f"validation_error.{field}"
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=422,
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        loc = ".".join(str(l) for l in error["loc"]) if error["loc"] else "body"
        msg = error["msg"]
        errors.append({
            "field": loc,
            "message": msg,
            "type": error["type"],
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Validation failed",
            "details": errors,
        },
    )


async def http_exception_handler_custom(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Handle HTTP exceptions with custom formatting."""
    if isinstance(exc.detail, dict):
        detail = exc.detail
    else:
        detail = {
            "error": "http_error",
            "message": str(exc.detail),
        }

    return JSONResponse(
        status_code=exc.status_code,
        content=detail,
        headers=exc.headers,
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
        },
    )


def setup_exception_handlers(app):
    """Set up exception handlers for the FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler_custom)
    app.add_exception_handler(Exception, general_exception_handler)


def format_validation_error(field: str, message: str) -> dict:
    """Format a validation error for API response."""
    return {
        "field": field,
        "message": message,
        "type": "value_error",
    }
