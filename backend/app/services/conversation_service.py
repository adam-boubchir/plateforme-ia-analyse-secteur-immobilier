from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.entities.conversation import (
    Conversation,
)

from app.database.repositories.conversation_repository import (
    ConversationRepository,
)


class ConversationService:
    """
    Service responsible for managing conversations.

    Responsibilities
    ----------------
    • Create conversations
    • Retrieve conversations
    • Update conversation metadata
    • Rename conversations
    • Delete conversations
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.repository = ConversationRepository(
            db
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        title: str | None = None,
        user_id: str | None = None,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        now = datetime.utcnow()

        conversation = Conversation(

            conversation_uuid=str(
                uuid4()
            ),

            title=title,

            user_id=user_id,

            status="ACTIVE",

            created_at=now,

            updated_at=now,

            last_message_at=now,

        )

        self.repository.create(
            conversation
        )

        self.db.commit()

        self.db.refresh(
            conversation
        )

        return conversation

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve one conversation by ID.
        """

        return self.repository.get_by_id(
            conversation_id
        )

    def get_by_uuid(
        self,
        conversation_uuid: str,
    ) -> Conversation | None:
        """
        Retrieve one conversation by UUID.
        """

        return self.repository.get_by_uuid(
            conversation_uuid
        )

    def get_all(
        self,
    ) -> list[Conversation]:
        """
        Retrieve every conversation.
        """

        return self.repository.get_all()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def rename(
        self,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        Rename a conversation.
        """

        conversation.title = title

        conversation.updated_at = (
            datetime.utcnow()
        )

        self.repository.update(
            conversation
        )

        self.db.commit()

        self.db.refresh(
            conversation
        )

        return conversation

    def update_title(
        self,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        Alias for rename().
        """

        return self.rename(

            conversation,

            title,

        )

    def update_last_message(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """
        Update conversation activity timestamp.
        """

        now = datetime.utcnow()

        conversation.last_message_at = now

        conversation.updated_at = now

        self.repository.update(
            conversation
        )

        self.db.commit()

        self.db.refresh(
            conversation
        )

        return conversation

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Delete a conversation.
        """

        self.repository.delete(
            conversation
        )

        self.db.commit()