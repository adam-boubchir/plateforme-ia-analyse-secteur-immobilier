from __future__ import annotations

from datetime import datetime

from app.logging.execution_context import (
    ExecutionContext,
)
from app.services.log_service import (
    LogService,
)

__all__ = (
    "ExecutionLogger",
)


class ExecutionLogger:
    """
    Responsible for recording AI agent executions.

    Responsibilities
    ----------------
    - Create an execution context.
    - Measure execution duration.
    - Record execution status.
    - Persist execution logs.
    """

    def __init__(
        self,
        *,
        log_service: LogService,
    ) -> None:
        self._log_service = log_service

    # ==========================================================
    # START
    # ==========================================================

    def start(
        self,
        *,
        question: str,
        conversation_id: int | None = None,
    ) -> ExecutionContext:
        """
        Create a new execution context.

        Args:
            question:
                User question.

            conversation_id:
                Conversation identifier.

        Returns:
            Newly created execution context.
        """

        context = ExecutionContext(
            conversation_id=conversation_id,
            question=question,
        )

        context.started_at = datetime.utcnow()
        context.status = "RUNNING"

        return context

    # ==========================================================
    # SUCCESS
    # ==========================================================

    def finish(
        self,
        *,
        context: ExecutionContext,
    ) -> None:
        """
        Finalize a successful execution.

        Args:
            context:
                Execution context.
        """

        self._finalize(
            context=context,
        )

        context.status = "SUCCESS"

        self.save(
            context=context,
        )

    # ==========================================================
    # FAILURE
    # ==========================================================

    def fail(
        self,
        *,
        context: ExecutionContext,
        error: Exception | str,
    ) -> None:
        """
        Finalize a failed execution.

        Args:
            context:
                Execution context.

            error:
                Raised exception or error message.
        """

        self._finalize(
            context=context,
        )

        context.status = "FAILED"
        context.error = str(
            error,
        )

        self.save(
            context=context,
        )

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        *,
        context: ExecutionContext,
    ) -> None:
        """
        Persist an execution log.

        Args:
            context:
                Execution context.
        """

        if context.conversation_id is None:
            raise ValueError(
                "ExecutionContext.conversation_id cannot be None.",
            )

        self._log_service.save_execution(
            context=context,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _finalize(
        *,
        context: ExecutionContext,
    ) -> None:
        """
        Compute execution duration.

        Args:
            context:
                Execution context.
        """

        context.finished_at = datetime.utcnow()

        if context.started_at is None:
            return

        execution_time = (
            context.finished_at
            - context.started_at
        ).total_seconds()

        context.execution_time = execution_time
        context.execution_time_ms = int(
            execution_time * 1000,
        )