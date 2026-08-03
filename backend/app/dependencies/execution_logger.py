from __future__ import annotations

from sqlalchemy.orm import Session

from app.dependencies.log import (
    get_log_service,
)
from app.logging.execution_logger import (
    ExecutionLogger,
)

__all__ = (
    "get_execution_logger",
)


def get_execution_logger(
    *,
    db: Session,
) -> ExecutionLogger:
    """
    Build and return an ExecutionLogger.
    """

    log_service = get_log_service(
        db=db,
    )

    return ExecutionLogger(
        log_service=log_service,
    )