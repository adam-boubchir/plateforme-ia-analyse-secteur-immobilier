from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import (
    Session,
)

from app.database.entities.conversation_message import (
    ConversationMessage,
)
from app.database.repositories.conversation_message_repository import (
    ConversationMessageRepository,
)

__all__ = (
    "ConversationMessageService",
)

# ==========================================================
# CONSTANTS
# ==========================================================

_USER_ROLE = "USER"
_ASSISTANT_ROLE = "ASSISTANT"
_COMPLETED_STATUS = "COMPLETED"


class ConversationMessageService:
    """
    Service responsible for managing conversation messages.

    Responsibilities:
        - Store user messages.
        - Store assistant messages.
        - Retrieve conversation history.
        - Delete conversation messages.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        """
        Initialize the conversation message service.

        Args:
            db:
                Application database session.
        """

        self._db = db

        self._repository = ConversationMessageRepository(
            db=db,
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def add_user_message(
        self,
        *,
        conversation_id: int,
        content: str,
    ) -> ConversationMessage:
        """
        Store a user message.

        Args:
            conversation_id:
                Conversation identifier.

            content:
                User message.

        Returns:
            Newly created message.
        """

        message = self._create_message(
            conversation_id=conversation_id,
            role=_USER_ROLE,
            content=content,
        )

        return message

    def add_assistant_message(
        self,
        *,
        conversation_id: int,
        content: str,
        generated_sql: str | None = None,
        execution_time_ms: int | None = None,
        rows_returned: int | None = None,
        rows: list[dict[str, object]] | None = None,
        pdf_path: str | None = None,
    ) -> ConversationMessage:
        """
        Store an assistant message.

        Args:
            conversation_id:
                Conversation identifier.

            content:
                Assistant response.

            generated_sql:
                Generated SQL query.

            execution_time_ms:
                SQL execution time.

            rows_returned:
                Number of returned rows.

            rows:
                Query result rows.

        Returns:
            Newly created message.
        """

        message = self._create_message(
            conversation_id=conversation_id,
            role=_ASSISTANT_ROLE,
            content=content,
            generated_sql=generated_sql,
            execution_time_ms=execution_time_ms,
            rows_returned=rows_returned,
            rows=rows,
            pdf_path=pdf_path,
        )

        return message

    # ==========================================================
    # READ
    # ==========================================================

    def get_messages(
        self,
        *,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """
        Retrieve every message of a conversation.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Conversation history.
        """

        messages = self._repository.get_by_conversation(
            conversation_id=conversation_id,
        )

        return messages

    def count_messages(
        self,
        *,
        conversation_id: int,
    ) -> int:
        """
        Count the number of messages in a conversation.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Number of messages.
        """

        count = self._repository.count_messages(
            conversation_id=conversation_id,
        )

        return count

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_message(
        self,
        *,
        message: ConversationMessage,
    ) -> None:
        """
        Delete one message.

        Args:
            message:
                Message entity.
        """

        self._repository.delete(
            message=message,
        )

        self._db.commit()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_message(
        self,
        *,
        conversation_id: int,
        role: str,
        content: str,
        generated_sql: str | None = None,
        execution_time_ms: int | None = None,
        rows_returned: int | None = None,
        rows: list[dict[str, object]] | None = None,
        pdf_path: str | None = None,
    ) -> ConversationMessage:
        """
        Create and persist one conversation message.

        Args:
            conversation_id:
                Conversation identifier.

            role:
                Message role.

            content:
                Message content.

            generated_sql:
                Generated SQL query.

            execution_time_ms:
                SQL execution time.

            rows_returned:
                Number of returned rows.

            rows:
                Query result rows.

        Returns:
            Persisted message.
        """

        result_json = self._serialize_rows(
            rows=rows,
        )

        message = ConversationMessage(
            conversation_id=conversation_id,
            request_id=str(uuid4()),
            role=role,
            content=content,
            generated_sql=generated_sql,
            result_json=result_json,
            pdf_path=pdf_path,
            execution_time_ms=execution_time_ms,
            rows_returned=rows_returned,
            status=_COMPLETED_STATUS,
            created_at=datetime.utcnow(),
        )

        self._repository.create(
            message=message,
        )

        self._commit_and_refresh(
            message=message,
        )

        created_message = message

        return created_message

    @staticmethod
    def _serialize_rows(
        *,
        rows: list[dict[str, object]] | None,
    ) -> str | None:
        """
        Serialize SQL query results into JSON.

        Args:
            rows:
                Query result rows.

        Returns:
            JSON representation or None.
        """

        if rows is None:
            return None

        serialized_rows = json.dumps(
            rows,
            ensure_ascii=False,
            default=str,
        )

        return serialized_rows

    def _commit_and_refresh(
        self,
        *,
        message: ConversationMessage,
    ) -> None:
        """
        Commit the transaction and refresh the entity.

        Args:
            message:
                Message entity.
        """

        self._db.commit()

        self._db.refresh(
            message,
        )