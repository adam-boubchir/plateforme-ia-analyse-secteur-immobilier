from datetime import datetime
import json
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

    USER_ROLE = "USER"
    ASSISTANT_ROLE = "ASSISTANT"
    COMPLETED_STATUS = "COMPLETED"

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db: Session = db

        self.repository: ConversationMessageRepository = (
            ConversationMessageRepository(
                db=db,
            )
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def add_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> ConversationMessage:
        """
        Store a user message.
        """

        return self._create_message(
            conversation_id=conversation_id,
            role=self.USER_ROLE,
            content=content,
        )

    def add_assistant_message(
        self,
        conversation_id: int,
        content: str,
        generated_sql: str | None = None,
        execution_time_ms: int | None = None,
        rows_returned: int | None = None,
        rows: list[dict] | None = None,
    ) -> ConversationMessage:
        """
        Store an assistant message.
        """

        return self._create_message(
            conversation_id=conversation_id,
            role=self.ASSISTANT_ROLE,
            content=content,
            generated_sql=generated_sql,
            execution_time_ms=execution_time_ms,
            rows_returned=rows_returned,
            rows=rows,
        )

    # ==========================================================
    # READ
    # ==========================================================

    def get_messages(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """
        Return every message of a conversation.
        """

        return self.repository.get_by_conversation(
            conversation_id=conversation_id,
        )

    def count_messages(
        self,
        conversation_id: int,
    ) -> int:
        """
        Return the number of messages.
        """

        return self.repository.count_messages(
            conversation_id=conversation_id,
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_message(
        self,
        message: ConversationMessage,
    ) -> None:
        """
        Delete one message.
        """

        self.repository.delete(
            message=message,
        )

        self.db.commit()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        generated_sql: str | None = None,
        execution_time_ms: int | None = None,
        rows_returned: int | None = None,
        rows: list[dict] | None = None,
    ) -> ConversationMessage:
        """
        Create and persist one message.
        """

        message = ConversationMessage(
            conversation_id=conversation_id,
            request_id=str(uuid4()),
            role=role,
            content=content,
            generated_sql=generated_sql,
            result_json=(
                json.dumps(
                    rows,
                    ensure_ascii=False,
                    default=str,
                )
                if rows is not None
                else None
            ),
            execution_time_ms=execution_time_ms,
            rows_returned=rows_returned,
            status=self.COMPLETED_STATUS,
            created_at=datetime.utcnow(),
        )

        self.repository.create(
            message=message,
        )

        self._commit_and_refresh(
            message=message,
        )

        return message

    def _commit_and_refresh(
        self,
        message: ConversationMessage,
    ) -> None:
        """
        Commit the transaction and refresh the entity.
        """

        self.db.commit()

        self.db.refresh(
            message,
        )


__all__ = [
    "ConversationMessageService",
]