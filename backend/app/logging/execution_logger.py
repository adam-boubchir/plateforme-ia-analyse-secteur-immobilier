from datetime import datetime

from app.logging.execution_context import (
    ExecutionContext,
)

from app.services.log_service import (
    LogService,
)


class ExecutionLogger:
    """
    Responsible for recording AI agent executions.

    Responsibilities
    ----------------
    • Create an execution context
    • Measure execution time
    • Mark execution status
    • Persist execution logs
    """

    def __init__(
        self,
        log_service: LogService,
    ) -> None:

        self.log_service = log_service

    # ==========================================================
    # START
    # ==========================================================

    def start(
        self,
        question: str,
        conversation_id: int | None = None,
    ) -> ExecutionContext:
        """
        Create a new execution context.
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
        context: ExecutionContext,
    ) -> None:
        """
        Finalize a successful execution.
        """

        self._finalize(context)

        context.status = "SUCCESS"

        self.save(context)

    # ==========================================================
    # FAILURE
    # ==========================================================

    def fail(
        self,
        context: ExecutionContext,
        error: Exception | str,
    ) -> None:
        """
        Finalize a failed execution.
        """

        self._finalize(context)

        context.status = "FAILED"

        context.error = str(error)

        self.save(context)

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Persist the execution.
        """

        if context.conversation_id is None:

            raise ValueError(
                "ExecutionContext.conversation_id cannot be None."
            )

        self.log_service.save_execution(
            context
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _finalize(
        context: ExecutionContext,
    ) -> None:
        """
        Compute execution duration.
        """

        context.finished_at = datetime.utcnow()

        if context.started_at is None:
            return

        context.execution_time = (
            context.finished_at
            - context.started_at
        ).total_seconds()

        context.execution_time_ms = int(
            context.execution_time * 1000
        )