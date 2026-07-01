from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.entities.conversation_message import (
    ConversationMessage,
)

from app.database.repositories.conversation_message_repository import (
    ConversationMessageRepository,
)


class ConversationMessageService:
    """
    Service responsible for managing conversation messages.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.repository = ConversationMessageRepository(db)

    def add_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> ConversationMessage:
        """
        Add a user message.
        """

        message = ConversationMessage(

            conversation_id=conversation_id,

            request_id=str(uuid4()),

            role="USER",

            content=content,

            generated_sql=None,

            execution_time_ms=None,

            rows_returned=None,

            status="COMPLETED",

            created_at=datetime.utcnow(),

        )

        self.repository.create(message)

        self.db.commit()

        self.db.refresh(message)

        return message

    def add_assistant_message(
        self,
        conversation_id: int,
        content: str,
        generated_sql: str | None = None,
        execution_time_ms: int | None = None,
        rows_returned: int | None = None,
    ) -> ConversationMessage:
        """
        Add an assistant message.
        """

        message = ConversationMessage(

            conversation_id=conversation_id,

            request_id=str(uuid4()),

            role="ASSISTANT",

            content=content,

            generated_sql=generated_sql,

            execution_time_ms=execution_time_ms,

            rows_returned=rows_returned,

            status="COMPLETED",

            created_at=datetime.utcnow(),

        )

        self.repository.create(message)

        self.db.commit()

        self.db.refresh(message)

        return message

    def get_messages(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """
        Return all messages of a conversation.
        """

        return self.repository.get_by_conversation(
            conversation_id
        )

    def count_messages(
        self,
        conversation_id: int,
    ) -> int:
        """
        Return the number of messages.
        """

        return self.repository.count_messages(
            conversation_id
        )

    def delete_message(
        self,
        message: ConversationMessage,
    ) -> None:
        """
        Delete one message.
        """

        self.repository.delete(message)

        self.db.commit()