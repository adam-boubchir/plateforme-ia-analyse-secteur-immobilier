from sqlalchemy.orm import Session

from app.services.conversation_message_service import (
    ConversationMessageService,
)


def get_conversation_message_service(
    db: Session,
) -> ConversationMessageService:
    """
    Dependency returning the ConversationMessageService.
    """

    return ConversationMessageService(db)