from __future__ import annotations

from app.database.entities.conversation_log import (
    ConversationLog,
)
from app.database.repositories.conversation_log_repository import (
    ConversationLogRepository,
)
from app.logging.execution_context import (
    ExecutionContext,
)

__all__ = (
    "LogService",
)


class LogService:
    """
    Service responsible for persisting and retrieving
    SQL Agent execution logs.
    """

    RUNNING_STATUS = "RUNNING"

    def __init__(
        self,
        *,
        repository: ConversationLogRepository,
    ) -> None:
        self._repository = repository

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_log(
        self,
        *,
        conversation_id: int,
        question: str,
    ) -> ConversationLog:
        """
        Create an empty execution log.

        Args:
            conversation_id:
                Conversation identifier.

            question:
                User question.

        Returns:
            Newly created log.
        """

        log = ConversationLog(
            conversation_id=conversation_id,
            question=question,
            status=self.RUNNING_STATUS,
        )

        created_log = self._repository.create(
            log=log,
        )

        return created_log

    # ==========================================================
    # SAVE EXECUTION
    # ==========================================================

    def save_execution(
        self,
        *,
        context: ExecutionContext,
    ) -> ConversationLog:
        """
        Persist a complete execution context.

        Args:
            context:
                Execution context.

        Returns:
            Persisted execution log.
        """

        if context.conversation_id is None:
            raise ValueError(
                "conversation_id cannot be None.",
            )

        log = ConversationLog(
            conversation_id=context.conversation_id,
            message_id=getattr(
                context,
                "message_id",
                None,
            ),
            question=context.question,
            selected_tables=context.selected_tables,
            business_knowledge=context.business_knowledge,
            join_knowledge=context.join_knowledge,
            forbidden_joins=context.forbidden_joins,
            semantic_context=context.semantic_context,
            sql_patterns=getattr(
                context,
                "sql_patterns",
                None,
            ),
            full_context=context.full_context,
            prompt=context.prompt,
            generated_sql=context.generated_sql,
            validated_sql=context.validated_sql,
            sql_result=context.sql_result,
            formatted_answer=context.formatted_answer,
            execution_time_ms=context.execution_time_ms,
            status=context.status,
            error_message=(
                context.error_message
                or context.error
            ),
        )

        created_log = self._repository.create(
            log=log,
        )

        return created_log

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_log(
        self,
        *,
        log: ConversationLog,
        **fields,
    ) -> ConversationLog:
        """
        Update one execution log.

        Args:
            log:
                Execution log.

            **fields:
                Fields to update.

        Returns:
            Updated log.
        """

        for key, value in fields.items():
            setattr(
                log,
                key,
                value,
            )

        updated_log = self._repository.update(
            log=log,
        )

        return updated_log

    # ==========================================================
    # READ
    # ==========================================================

    def get_log(
        self,
        *,
        log_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve one execution log.
        """

        log = self._repository.get_by_id(
            log_id=log_id,
        )

        return log

    def get_logs_by_conversation(
        self,
        *,
        conversation_id: int,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution of one conversation.
        """

        logs = self._repository.get_by_conversation(
            conversation_id=conversation_id,
        )

        return logs

    def get_last_log(
        self,
        *,
        conversation_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve the latest execution of one conversation.
        """

        log = self._repository.get_last_by_conversation(
            conversation_id=conversation_id,
        )

        return log

    def count_logs(
        self,
        *,
        conversation_id: int,
    ) -> int:
        """
        Count executions of one conversation.
        """

        count = self._repository.count_by_conversation(
            conversation_id=conversation_id,
        )

        return count

    def get_all_logs(
        self,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log.
        """

        logs = self._repository.get_all()

        return logs

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_log(
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

        self._repository.delete(
            entity=log,
        )