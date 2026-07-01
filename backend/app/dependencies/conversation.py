from sqlalchemy.orm import Session

from app.services.conversation_service import (
    ConversationService,
)


def get_conversation_service(
    db: Session,
) -> ConversationService:
    """
    Dependency returning the ConversationService.
    """

    return ConversationService(db)