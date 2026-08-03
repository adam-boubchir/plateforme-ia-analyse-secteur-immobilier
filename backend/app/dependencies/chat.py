from __future__ import annotations

from typing import Annotated

from fastapi import (
    Depends,
)
from sqlalchemy.orm import (
    Session,
)

from app.dependencies.conversation import (
    get_conversation_service,
)
from app.dependencies.conversation_message import (
    get_conversation_message_service,
)
from app.dependencies.database import (
    get_immo_db,
    get_ministry_db,
)
from app.dependencies.orchestrator import (
    get_orchestrator_service,
)
from app.services.chat_service import (
    ChatService,
)

__all__ = (
    "get_chat_service",
)

# ==========================================================
# TYPE ALIASES
# ==========================================================

ImmoDatabase = Annotated[
    Session,
    Depends(get_immo_db),
]

MinistryDatabase = Annotated[
    Session,
    Depends(get_ministry_db),
]

# ==========================================================
# CHAT SERVICE
# ==========================================================


def get_chat_service(
    *,
    immo_db: ImmoDatabase,
    ministry_db: MinistryDatabase,
) -> ChatService:
    """
    Build and return a fully configured ChatService.

    This factory assembles every service required
    to process a user request through the AI platform.

    Args:
        immo_db:
            Session connected to the application database.

        ministry_db:
            Session connected to the Ministry database.

    Returns:
        Configured ChatService instance.
    """

    orchestrator_service = get_orchestrator_service(
        immo_db=immo_db,
        ministry_db=ministry_db,
    )

    conversation_service = get_conversation_service(
        db=immo_db,
    )

    message_service = get_conversation_message_service(
        db=immo_db,
    )

    chat_service = ChatService(
        orchestrator_service=orchestrator_service,
        conversation_service=conversation_service,
        message_service=message_service,
    )

    return chat_service