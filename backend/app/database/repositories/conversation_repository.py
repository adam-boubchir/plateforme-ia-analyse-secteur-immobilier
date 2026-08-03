from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.conversation import Conversation
from app.database.repositories.base_repository import BaseRepository

__all__ = [
    "ConversationRepository",
]


class ConversationRepository(BaseRepository):
    """
    Repository responsible for Conversation persistence.
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
        conversation: Conversation,
    ) -> Conversation:
        """
        Persist a new conversation.
        """

        self.add(
            entity=conversation,
        )

        self.flush()

        return conversation

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        *,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its ID.
        """

        statement = (
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
            )
        )

        return self._db.scalar(statement)

    def get_by_uuid(
        self,
        *,
        conversation_uuid: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its UUID.
        """

        statement = (
            select(Conversation)
            .where(
                Conversation.conversation_uuid == conversation_uuid,
            )
        )

        return self._db.scalar(statement)

    def get_all(
        self,
    ) -> list[Conversation]:
        """
        Retrieve every conversation ordered by last activity.
        """

        statement = (
            select(Conversation)
            .order_by(
                Conversation.last_message_at.desc(),
            )
        )

        return list(
            self._db.scalars(statement)
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        *,
        conversation: Conversation,
    ) -> Conversation:
        """
        Flush pending modifications.
        """

        self.flush()

        return conversation

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        *,
        conversation: Conversation,
    ) -> None:
        """
        Delete a conversation.
        """

        super().delete(
            entity=conversation,
        )