from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.conversation import (
    Conversation,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


class ConversationRepository(BaseRepository):
    """
    Repository responsible for Conversation persistence.
    """

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(db)

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """
        Persist a new conversation.
        """

        self.add(
            conversation
        )

        self.flush()

        return conversation

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its ID.
        """

        return self.db.scalar(

            select(
                Conversation
            ).where(
                Conversation.id == conversation_id
            )

        )

    def get_by_uuid(
        self,
        conversation_uuid: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its UUID.
        """

        return self.db.scalar(

            select(
                Conversation
            ).where(
                Conversation.conversation_uuid
                == conversation_uuid
            )

        )

    def get_all(
        self,
    ) -> list[Conversation]:
        """
        Retrieve every conversation ordered by last activity.
        """

        return list(

            self.db.scalars(

                select(
                    Conversation
                ).order_by(
                    Conversation.last_message_at.desc()
                )

            )

        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """
        Flush pending changes.
        """

        self.flush()

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

        self.db.delete(
            conversation
        )