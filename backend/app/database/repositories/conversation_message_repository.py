from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.entities.conversation_message import (
    ConversationMessage,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)

__all__ = [
    "ConversationMessageRepository",
]


class ConversationMessageRepository(BaseRepository):
    """
    Repository responsible for ConversationMessage persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(db=db)

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        *,
        message: ConversationMessage,
    ) -> ConversationMessage:
        """
        Persist a new conversation message.
        """

        self.add(
            entity=message,
        )

        self.flush()

        return message

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        *,
        message_id: int,
    ) -> ConversationMessage | None:
        """
        Retrieve one message by its ID.
        """

        statement = (
            select(ConversationMessage)
            .where(
                ConversationMessage.id == message_id,
            )
        )

        return self._db.scalar(statement)

    def get_by_conversation(
        self,
        *,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """
        Retrieve all messages of one conversation.
        """

        statement = (
            select(ConversationMessage)
            .where(
                ConversationMessage.conversation_id == conversation_id,
            )
            .order_by(
                ConversationMessage.created_at.asc(),
            )
        )

        return list(
            self._db.scalars(statement)
        )

    def count_messages(
        self,
        *,
        conversation_id: int,
    ) -> int:
        """
        Return the number of messages of one conversation.
        """

        statement = (
            select(func.count())
            .select_from(ConversationMessage)
            .where(
                ConversationMessage.conversation_id == conversation_id,
            )
        )

        return self._db.scalar(statement) or 0

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        *,
        message: ConversationMessage,
    ) -> ConversationMessage:
        """
        Flush pending modifications.
        """

        self.flush()

        return message

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        *,
        message: ConversationMessage,
    ) -> None:
        """
        Delete one message.
        """

        super().delete(
            entity=message,
        )