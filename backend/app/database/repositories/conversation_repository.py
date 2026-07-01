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

    def create(
        self,
        conversation: Conversation,
    ) -> Conversation:

        self.add(conversation)

        self.flush()

        return conversation

    def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        return self.db.scalar(

            select(Conversation)

            .where(
                Conversation.id == conversation_id
            )

        )

    def get_by_uuid(
        self,
        conversation_uuid: str,
    ) -> Conversation | None:

        return self.db.scalar(

            select(Conversation)

            .where(
                Conversation.conversation_uuid
                == conversation_uuid
            )

        )

    def get_all(
        self,
    ) -> list[Conversation]:

        return list(

            self.db.scalars(

                select(Conversation)

                .order_by(
                    Conversation.last_message_at.desc()
                )

            )

        )

    def update(
        self,
        conversation: Conversation,
    ) -> Conversation:

        self.flush()

        return conversation

    def delete(
        self,
        conversation: Conversation,
    ) -> None:

        self.db.delete(conversation)