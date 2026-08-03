from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.entities.conversation_log import (
    ConversationLog,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)

__all__ = (
    "ConversationLogRepository",
)


class ConversationLogRepository(BaseRepository):
    """
    Repository responsible for ConversationLog persistence.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        *,
        log: ConversationLog,
    ) -> ConversationLog:
        """
        Persist a new execution log.

        Args:
            log:
                Execution log.

        Returns:
            Persisted execution log.
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
        *,
        log_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve one execution log.

        Args:
            log_id:
                Log identifier.

        Returns:
            Matching execution log or None.
        """

        statement = (
            select(
                ConversationLog,
            )
            .where(
                ConversationLog.id == log_id,
            )
        )

        log = self._db.scalar(
            statement,
        )

        return log

    def get_by_conversation(
        self,
        *,
        conversation_id: int,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log of one conversation.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Ordered execution logs.
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

        logs = list(
            self._db.scalars(
                statement,
            )
        )

        return logs

    def get_last_by_conversation(
        self,
        *,
        conversation_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve the latest execution log of one conversation.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Latest execution log or None.
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
            .limit(
                1,
            )
        )

        log = self._db.scalar(
            statement,
        )

        return log

    def count_by_conversation(
        self,
        *,
        conversation_id: int,
    ) -> int:
        """
        Count execution logs of one conversation.

        Args:
            conversation_id:
                Conversation identifier.

        Returns:
            Number of execution logs.
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

        count = self._db.scalar(
            statement,
        ) or 0

        return count

    def get_all(
        self,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log.

        Returns:
            Ordered execution logs.
        """

        statement = (
            select(
                ConversationLog,
            )
            .order_by(
                ConversationLog.created_at.desc(),
            )
        )

        logs = list(
            self._db.scalars(
                statement,
            )
        )

        return logs

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        *,
        log: ConversationLog,
    ) -> ConversationLog:
        """
        Flush pending changes.

        Args:
            log:
                Updated execution log.

        Returns:
            Updated execution log.
        """

        self.flush()

        return log

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        *,
        log: ConversationLog,
    ) -> None:
        """
        Delete one execution log.

        Args:
            log:
                Execution log to delete.
        """

        super().delete(
            entity=log,
        )