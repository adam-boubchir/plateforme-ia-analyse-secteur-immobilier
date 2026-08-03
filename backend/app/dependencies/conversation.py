from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import (
    get_immo_db,
)
from app.services.conversation_service import (
    ConversationService,
)

__all__ = (
    "get_conversation_service",
)


# ==========================================================
# TYPE ALIASES
# ==========================================================

DatabaseSession = Annotated[
    Session,
    Depends(get_immo_db),
]


# ==========================================================
# CONVERSATION SERVICE
# ==========================================================

def get_conversation_service(
    db: DatabaseSession,
) -> ConversationService:
    """
    Build and return the ConversationService.

    Args:
        db:
            Application database session.

    Returns:
        A configured ConversationService.
    """

    conversation_service = ConversationService(
        db=db,
    )

    return conversation_service