from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.repositories.conversation_log_repository import (
    ConversationLogRepository,
)
from app.database.session import (
    get_immo_db,
)
from app.services.log_service import (
    LogService,
)

__all__ = (
    "get_log_service",
)


# ==========================================================
# TYPE ALIASES
# ==========================================================

DatabaseSession = Annotated[
    Session,
    Depends(get_immo_db),
]


# ==========================================================
# LOG SERVICE
# ==========================================================

def get_log_service(
    db: DatabaseSession,
) -> LogService:
    """
    Build and return the LogService.

    Args:
        db:
            Application database session.

    Returns:
        A configured LogService.
    """

    repository = ConversationLogRepository(
        db=db,
    )

    return LogService(
        repository=repository,
    )