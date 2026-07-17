from sqlalchemy import (
    select,
)

from sqlalchemy.orm import (
    Session,
)

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
    ):

        super().__init__(db)

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

        self.add(log)

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

        return self.db.scalar(

            select(
                ConversationLog
            ).where(
                ConversationLog.id == log_id
            )

        )

    def get_by_conversation(
        self,
        conversation_id: int,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log of one conversation.
        """

        return list(

            self.db.scalars(

                select(
                    ConversationLog
                )

                .where(
                    ConversationLog.conversation_id
                    == conversation_id
                )

                .order_by(
                    ConversationLog.created_at.desc()
                )

            )

        )

    def get_last_by_conversation(
        self,
        conversation_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve the latest execution of one conversation.
        """

        return self.db.scalar(

            select(
                ConversationLog
            )

            .where(
                ConversationLog.conversation_id
                == conversation_id
            )

            .order_by(
                ConversationLog.created_at.desc()
            )

            .limit(1)

        )

    def count_by_conversation(
        self,
        conversation_id: int,
    ) -> int:
        """
        Return the number of executions
        of one conversation.
        """

        return len(

            self.get_by_conversation(
                conversation_id
            )

        )

    def get_all(
        self,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log.
        """

        return list(

            self.db.scalars(

                select(
                    ConversationLog
                )

                .order_by(
                    ConversationLog.created_at.desc()
                )

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

        self.db.delete(log)