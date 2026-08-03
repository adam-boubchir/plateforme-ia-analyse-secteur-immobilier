from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.conversation_message_service import (
    ConversationMessageService,
)

__all__ = (
    "get_conversation_message_service",
)


# ==========================================================
# CONVERSATION MESSAGE SERVICE
# ==========================================================

def get_conversation_message_service(
    *,
    db: Session,
) -> ConversationMessageService:
    """
    Build and return the ConversationMessageService.

    Args:
        db:
            Application database session.

    Returns:
        A configured ConversationMessageService.
    """

    conversation_message_service = ConversationMessageService(
        db=db,
    )

    return conversation_message_service