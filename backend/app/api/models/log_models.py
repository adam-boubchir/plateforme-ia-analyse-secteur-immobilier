from datetime import datetime
from typing import Any

from pydantic import BaseModel


# ==========================================================
# Log Summary
# ==========================================================

class LogSummaryResponse(BaseModel):
    """
    Summary displayed in the logs list.
    """

    id: int

    conversation_id: int

    question: str

    status: str

    execution_time_ms: int | None = None

    created_at: datetime


# ==========================================================
# Log Details
# ==========================================================

class LogDetailsResponse(BaseModel):
    """
    Complete execution details.
    """

    id: int

    conversation_id: int

    message_id: int | None = None

    question: str

    selected_tables: str | None = None

    business_knowledge: str | None = None

    join_knowledge: str | None = None

    forbidden_joins: str | None = None

    semantic_context: str | None = None

    sql_patterns: str | None = None

    full_context: str | None = None

    prompt: str | None = None

    generated_sql: str | None = None

    validated_sql: str | None = None

    sql_result: Any | None = None

    formatted_answer: str | None = None

    execution_time_ms: int | None = None

    status: str

    error_message: str | None = None

    created_at: datetime


# ==========================================================
# Logs List Response
# ==========================================================

class LogsResponse(BaseModel):
    """
    Response returned by GET /logs
    """

    success: bool

    logs: list[LogSummaryResponse]


# ==========================================================
# One Log Response
# ==========================================================

class LogResponse(BaseModel):
    """
    Response returned by GET /logs/{id}
    """

    success: bool

    log: LogDetailsResponse