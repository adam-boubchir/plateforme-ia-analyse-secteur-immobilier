from sqlalchemy.orm import Session

from app.database.repositories.conversation_log_repository import (
    ConversationLogRepository,
)

from app.services.log_service import (
    LogService,
)


# ==========================================================
# LOG SERVICE
# ==========================================================

def get_log_service(
    db: Session,
) -> LogService:
    """
    Dependency responsible for creating the LogService.
    """

    return LogService(

        ConversationLogRepository(
            db
        )

    )