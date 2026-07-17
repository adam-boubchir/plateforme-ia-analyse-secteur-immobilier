from sqlalchemy import (
    func,
    select,
)
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

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        message: ConversationMessage,
    ) -> ConversationMessage:
        """
        Persist a new conversation message.
        """

        self.add(
            message
        )

        self.flush()

        return message

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        message_id: int,
    ) -> ConversationMessage | None:
        """
        Retrieve one message by its ID.
        """

        return self.db.scalar(

            select(
                ConversationMessage
            ).where(
                ConversationMessage.id == message_id
            )

        )

    def get_by_conversation(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """
        Retrieve all messages of one conversation.
        """

        return list(

            self.db.scalars(

                select(
                    ConversationMessage
                )

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
        """
        Return the number of messages of one conversation.
        """

        return self.db.scalar(

            select(
                func.count()
            )

            .select_from(
                ConversationMessage
            )

            .where(
                ConversationMessage.conversation_id
                == conversation_id
            )

        ) or 0

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
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
        message: ConversationMessage,
    ) -> None:
        """
        Delete one message.
        """

        self.db.delete(
            message
        )