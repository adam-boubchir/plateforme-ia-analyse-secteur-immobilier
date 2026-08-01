from app.database.entities.conversation_log import (
    ConversationLog,
)
from app.database.repositories.conversation_log_repository import (
    ConversationLogRepository,
)
from app.logging.execution_context import (
    ExecutionContext,
)


class LogService:
    """
    Service responsible for persisting and retrieving
    SQL Agent execution logs.
    """

    RUNNING_STATUS = "RUNNING"

    def __init__(
        self,
        repository: ConversationLogRepository,
    ) -> None:

        self.repository: ConversationLogRepository = repository

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_log(
        self,
        conversation_id: int,
        question: str,
    ) -> ConversationLog:
        """
        Create an empty execution log.
        """

        log = ConversationLog(
            conversation_id=conversation_id,
            question=question,
            status=self.RUNNING_STATUS,
        )

        return self.repository.create(
            log=log,
        )

    # ==========================================================
    # SAVE EXECUTION
    # ==========================================================

    def save_execution(
        self,
        context: ExecutionContext,
    ) -> ConversationLog:
        """
        Persist the complete execution context.
        """

        if context.conversation_id is None:
            raise ValueError(
                "conversation_id cannot be None."
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

        return self.repository.create(
            log=log,
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_log(
        self,
        log: ConversationLog,
        **fields,
    ) -> ConversationLog:
        """
        Update one execution log.
        """

        for key, value in fields.items():
            setattr(
                log,
                key,
                value,
            )

        return self.repository.update(
            log=log,
        )

    # ==========================================================
    # READ
    # ==========================================================

    def get_log(
        self,
        log_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve one execution log.
        """

        return self.repository.get_by_id(
            log_id=log_id,
        )

    def get_logs_by_conversation(
        self,
        conversation_id: int,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution of one conversation.
        """

        return self.repository.get_by_conversation(
            conversation_id=conversation_id,
        )

    def get_last_log(
        self,
        conversation_id: int,
    ) -> ConversationLog | None:
        """
        Retrieve the latest execution of one conversation.
        """

        return self.repository.get_last_by_conversation(
            conversation_id=conversation_id,
        )

    def count_logs(
        self,
        conversation_id: int,
    ) -> int:
        """
        Count executions of one conversation.
        """

        return self.repository.count_by_conversation(
            conversation_id=conversation_id,
        )

    def get_all_logs(
        self,
    ) -> list[ConversationLog]:
        """
        Retrieve every execution log.
        """

        return self.repository.get_all()

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_log(
        self,
        log: ConversationLog,
    ) -> None:
        """
        Delete one execution log.
        """

        self.repository.delete(
            log=log,
        )


__all__ = [
    "LogService",
]