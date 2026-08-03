from __future__ import annotations

import logging

from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.responses import (
    JSONResponse,
)

from app.agents.sql_agent.sql_executor import (
    SQLExecutionError,
)
from app.agents.sql_agent.sql_validator import (
    SQLValidationError,
)

__all__ = (
    "register_exception_handlers",
)

logger = logging.getLogger(__name__)


# ==========================================================
# PRIVATE
# ==========================================================

def _build_error_response(
    *,
    status_code: int,
    message: str,
) -> JSONResponse:
    """
    Build a standardized API error response.

    Args:
        status_code:
            HTTP status code.

        message:
            Error message returned to the client.

    Returns:
        A standardized JSONResponse.
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "conversation_uuid": None,
            "answer": "",
            "sql": None,
            "rows": [],
            "error": message,
        },
    )


# ==========================================================
# PUBLIC
# ==========================================================

def register_exception_handlers(
    *,
    app: FastAPI,
) -> None:
    """
    Register all global exception handlers.

    Args:
        app:
            FastAPI application instance.
    """

    @app.exception_handler(SQLValidationError)
    async def sql_validation_handler(
        request: Request,
        exc: SQLValidationError,
    ) -> JSONResponse:
        """
        Handle SQL validation errors.
        """

        logger.warning(
            "SQL validation failed: %s",
            exc,
        )

        return _build_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
        )

    @app.exception_handler(SQLExecutionError)
    async def sql_execution_handler(
        request: Request,
        exc: SQLExecutionError,
    ) -> JSONResponse:
        """
        Handle SQL execution errors.
        """

        logger.exception(
            "SQL execution failed.",
        )

        return _build_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="SQL execution failed.",
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request,
        exc: ValueError,
    ) -> JSONResponse:
        """
        Handle application value errors.
        """

        logger.warning(
            "%s",
            exc,
        )

        return _build_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle every unexpected exception.
        """

        logger.exception(
            "Unhandled exception.",
        )

        return _build_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error.",
        )