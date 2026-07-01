from sqlalchemy.orm import Session

from app.dependencies.sql_agent import (
    get_sql_agent,
)

from app.dependencies.conversation import (
    get_conversation_service,
)

from app.dependencies.conversation_message import (
    get_conversation_message_service,
)

from app.services.chat_service import (
    ChatService,
)


def get_chat_service(
    db: Session,
) -> ChatService:
    """
    Dependency returning the ChatService.
    """

    sql_agent = get_sql_agent(db)

    conversation_service = get_conversation_service(db)

    message_service = get_conversation_message_service(db)

    return ChatService(

        sql_agent=sql_agent,

        conversation_service=conversation_service,

        message_service=message_service,

    )