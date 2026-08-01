from __future__ import annotations

from app.database.entities.conversation_log import ConversationLog
from app.services.log_service import LogService

__all__ = ["ExecutionLogger"]


class ExecutionLogger:
    """
    High-level logger used by AI agents.

    This class provides semantic logging methods while delegating
    persistence operations to the LogService.
    """

    STATUS_SUCCESS = "SUCCESS"
    STATUS_ERROR = "ERROR"

    def __init__(
        self,
        log_service: LogService,
    ) -> None:
        self.log_service = log_service
        self.log: ConversationLog | None = None

    # ==========================================================
    # START
    # ==========================================================

    def start(
        self,
        conversation_id: int,
        question: str,
    ) -> None:
        """
        Create a new execution log.
        """

        self.log = self.log_service.create_log(
            conversation_id=conversation_id,
            question=question,
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        **fields,
    ) -> None:
        """
        Update the current execution log.
        """

        if self.log is None:
            return

        self.log = self.log_service.update_log(
            self.log,
            **fields,
        )

    # ==========================================================
    # SUCCESS
    # ==========================================================

    def success(self) -> None:
        """
        Mark the current execution as successful.
        """

        self.update(
            status=self.STATUS_SUCCESS,
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def error(
        self,
        message: str,
    ) -> None:
        """
        Mark the current execution as failed.
        """

        self.update(
            status=self.STATUS_ERROR,
            error_message=message,
        )