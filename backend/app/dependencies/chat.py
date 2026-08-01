from sqlalchemy.orm import Session

from app.dependencies.conversation import (
    get_conversation_service,
)
from app.dependencies.conversation_message import (
    get_conversation_message_service,
)
from app.dependencies.orchestrator import (
    get_orchestrator_service,
)
from app.services.chat_service import (
    ChatService,
)


def get_chat_service(
    immo_db: Session,
    ministry_db: Session,
) -> ChatService:
    """
    Dependency responsible for building the ChatService.
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

    return ChatService(
        orchestrator_service=orchestrator_service,
        conversation_service=conversation_service,
        message_service=message_service,
    )


__all__ = [
    "get_chat_service",
]