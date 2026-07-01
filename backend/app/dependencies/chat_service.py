from sqlalchemy.orm import Session

from app.dependencies.sql_agent import (
    get_sql_agent,
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

    return ChatService(sql_agent)