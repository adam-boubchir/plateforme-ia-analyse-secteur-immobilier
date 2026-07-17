from app.database.entities.conversation_log import (
    ConversationLog,
)

from app.services.log_service import (
    LogService,
)


class ExecutionLogger:
    """
    High-level logger used by AI agents.

    It abstracts the persistence layer and exposes
    semantic methods describing the execution pipeline.
    """

    def __init__(
        self,
        log_service: LogService,
    ):

        self.log_service = log_service

        self.log: ConversationLog | None = None

    # --------------------------------------------------
    # START
    # --------------------------------------------------

    def start(
        self,
        conversation_id: int,
        question: str,
    ) -> None:

        self.log = self.log_service.create_log(

            conversation_id=conversation_id,

            question=question,

        )

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(
        self,
        **fields,
    ) -> None:

        if self.log is None:

            return

        self.log = self.log_service.update_log(

            self.log,

            **fields,

        )

    # --------------------------------------------------
    # SUCCESS
    # --------------------------------------------------

    def success(
        self,
    ) -> None:

        self.update(

            status="SUCCESS",

        )

    # --------------------------------------------------
    # ERROR
    # --------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:

        self.update(

            status="ERROR",

            error_message=message,

        )