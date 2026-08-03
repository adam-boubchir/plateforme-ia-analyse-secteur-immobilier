from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import (
    Session,
)

from app.database.entities.conversation import (
    Conversation,
)
from app.database.repositories.conversation_repository import (
    ConversationRepository,
)

__all__ = (
    "ConversationService",
)

# ==========================================================
# CONSTANTS
# ==========================================================

_ACTIVE_STATUS = "ACTIVE"


class ConversationService:
    """
    Service responsible for managing conversations.

    Responsibilities:
        - Create conversations.
        - Retrieve conversations.
        - Rename conversations.
        - Update conversation metadata.
        - Delete conversations.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        """
        Initialize the conversation service.

        Args:
            db:
                Application database session.
        """

        self._db = db

        self._repository = ConversationRepository(
            db=db,
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        *,
        title: str | None = None,
        user_id: str | None = None,
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            title:
                Conversation title.

            user_id:
                Optional user identifier.

        Returns:
            Newly created conversation.
        """

        now = datetime.utcnow()

        conversation = Conversation(
            conversation_uuid=str(uuid4()),
            title=title,
            user_id=user_id,
            status=_ACTIVE_STATUS,
            created_at=now,
            updated_at=now,
            last_message_at=now,
        )

        self._repository.create(
            conversation=conversation,
        )

        self._commit_and_refresh(
            conversation=conversation,
        )

        created_conversation = conversation

        return created_conversation

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        *,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its identifier.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Matching conversation or None.
        """

        conversation = self._repository.get_by_id(
            conversation_id=conversation_id,
        )

        return conversation

    def get_by_uuid(
        self,
        *,
        conversation_uuid: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its UUID.

        Args:
            conversation_uuid:
                Conversation UUID.

        Returns:
            Matching conversation or None.
        """

        conversation = self._repository.get_by_uuid(
            conversation_uuid=conversation_uuid,
        )

        return conversation

    def get_all(
        self,
    ) -> list[Conversation]:
        """
        Retrieve every conversation.

        Returns:
            List of conversations.
        """

        conversations = self._repository.get_all()

        return conversations

    # ==========================================================
    # UPDATE
    # ==========================================================

    def rename(
        self,
        *,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        Rename a conversation.

        Args:
            conversation:
                Conversation entity.

            title:
                New conversation title.

        Returns:
            Updated conversation.
        """

        conversation.title = title

        self._touch(
            conversation=conversation,
        )

        self._repository.update(
            conversation=conversation,
        )

        self._commit_and_refresh(
            conversation=conversation,
        )

        updated_conversation = conversation

        return updated_conversation

    def update_title(
        self,
        *,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        Update the conversation title.

        Args:
            conversation:
                Conversation entity.

            title:
                New title.

        Returns:
            Updated conversation.
        """

        updated_conversation = self.rename(
            conversation=conversation,
            title=title,
        )

        return updated_conversation

    def update_last_message(
        self,
        *,
        conversation: Conversation,
    ) -> Conversation:
        """
        Update conversation activity timestamps.

        Args:
            conversation:
                Conversation entity.

        Returns:
            Updated conversation.
        """

        now = datetime.utcnow()

        conversation.last_message_at = now
        conversation.updated_at = now

        self._repository.update(
            conversation=conversation,
        )

        self._commit_and_refresh(
            conversation=conversation,
        )

        updated_conversation = conversation

        return updated_conversation

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

        Args:
            conversation:
                Conversation entity.
        """

        self._repository.delete(
            conversation=conversation,
        )

        self._db.commit()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _touch(
        *,
        conversation: Conversation,
    ) -> None:
        """
        Update the modification timestamp.

        Args:
            conversation:
                Conversation entity.
        """

        now = datetime.utcnow()

        conversation.updated_at = now

    def _commit_and_refresh(
        self,
        *,
        conversation: Conversation,
    ) -> None:
        """
        Commit the transaction and refresh the entity.

        Args:
            conversation:
                Conversation entity.
        """

        self._db.commit()

        self._db.refresh(
            conversation,
        )