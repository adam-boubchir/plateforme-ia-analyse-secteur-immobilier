from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.conversation_message import (
    ConversationMessage,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


class ConversationMessageRepository(BaseRepository):
    """
    Repository responsible for ConversationMessage persistence.
    """

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(db)

    def create(
        self,
        message: ConversationMessage,
    ) -> ConversationMessage:

        self.add(message)

        self.flush()

        return message

    def get_by_conversation(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:

        return list(

            self.db.scalars(

                select(ConversationMessage)

                .where(
                    ConversationMessage.conversation_id
                    == conversation_id
                )

                .order_by(
                    ConversationMessage.created_at.asc()
                )

            )

        )

    def count_messages(
        self,
        conversation_id: int,
    ) -> int:

        return len(

            self.get_by_conversation(
                conversation_id
            )

        )

    def delete(
        self,
        message: ConversationMessage,
    ) -> None:

        self.db.delete(message)