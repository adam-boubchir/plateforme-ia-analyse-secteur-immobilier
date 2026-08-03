from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

__all__ = (
    "ExecutionContext",
)


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution context used throughout the complete AI
    execution pipeline.

    This object is progressively enriched by each component
    (context builder, SQL generator, validator, executor,
    formatter, logger...) before finally being persisted into
    the conversation logs.
    """

    # ==========================================================
    # Conversation
    # ==========================================================

    conversation_id: int | None = None

    message_id: int | None = None

    request_id: str | None = None

    question: str = ""

    # ==========================================================
    # Knowledge Selection
    # ==========================================================

    selected_tables: str | None = None

    business_knowledge: str | None = None

    join_knowledge: str | None = None

    forbidden_joins: str |None = None

    semantic_context: str | None = None

    sql_patterns: str | None = None

    full_context: str | None = None

    # ==========================================================
    # Prompt
    # ==========================================================

    prompt: str | None = None

    # ==========================================================
    # SQL
    # ==========================================================

    generated_sql: str | None = None

    validated_sql: str | None = None

    # ==========================================================
    # SQL Result
    # ==========================================================

    sql_result: object | None = None

    formatted_answer: str | None = None

    rows_returned: int | None = None

    # ==========================================================
    # LLM
    # ==========================================================

    llm_provider: str | None = None

    llm_model: str | None = None

    token_input: int | None = None

    token_output: int | None = None

    # ==========================================================
    # Execution
    # ==========================================================

    started_at: datetime | None = None

    finished_at: datetime | None = None

    execution_time: float | None = None

    execution_time_ms: int | None = None

    # ==========================================================
    # Status
    # ==========================================================

    status: str = "RUNNING"

    error: str | None = None

    error_message: str | None = None