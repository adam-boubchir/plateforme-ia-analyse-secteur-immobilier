from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.orm import Session

from app.database.entities.conversation_log import (
    ConversationLog,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class ConversationLogRepository(BaseRepository):
    """
    Repository responsible for ConversationLog persistence.
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
        log: ConversationLog,
    ) -> ConversationLog:
        """
        Persist a new execution log.
        """

        self.add(
            entity=log,
        )

        self.flush()

        return log

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        log_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve one execution log.
        """

        statement = (
            select(
                ConversationLog,
            )
            .where(
                ConversationLog.id == log_id,
            )
        )

        return self.db.scalar(
            statement,
        )

    def get_by_conversation(
        self,
        conversation_id: int,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log of one conversation.
        """

        statement = (
            select(
                ConversationLog,
            )
            .where(
                ConversationLog.conversation_id == conversation_id,
            )
            .order_by(
                ConversationLog.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    def get_last_by_conversation(
        self,
        conversation_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve the latest execution log of one conversation.
        """

        statement = (
            select(
                ConversationLog,
            )
            .where(
                ConversationLog.conversation_id == conversation_id,
            )
            .order_by(
                ConversationLog.created_at.desc(),
            )
            .limit(1)
        )

        return self.db.scalar(
            statement,
        )

    def count_by_conversation(
        self,
        conversation_id: int,
    ) -> int:
        """
        Return the number of execution logs
        of one conversation.
        """

        statement = (
            select(
                func.count(),
            )
            .select_from(
                ConversationLog,
            )
            .where(
                ConversationLog.conversation_id == conversation_id,
            )
        )

        return self.db.scalar(
            statement,
        ) or 0

    def get_all(
        self,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log.
        """

        statement = (
            select(
                ConversationLog,
            )
            .order_by(
                ConversationLog.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        log: ConversationLog,
    ) -> ConversationLog:
        """
        Flush pending changes.
        """

        self.flush()

        return log

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        log: ConversationLog,
    ) -> None:
        """
        Delete one execution log.
        """

        self.db.delete(
            log,
        )


__all__ = [
    "ConversationLogRepository",
]