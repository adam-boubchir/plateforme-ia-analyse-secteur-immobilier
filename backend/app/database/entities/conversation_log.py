from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.entities.base import (
    Base,
)

__all__ = (
    "ConversationLog",
)


class ConversationLog(Base):
    """
    Database entity storing the complete execution trace
    of one AI request.

    One record corresponds to one execution of an AI agent.
    """

    __tablename__ = "conversation_logs"

    # ==========================================================
    # IDENTIFICATION
    # ==========================================================

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "conversations.id",
        ),
        nullable=False,
        index=True,
    )

    message_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "conversation_messages.id",
        ),
        nullable=True,
        index=True,
    )

    # ==========================================================
    # USER QUESTION
    # ==========================================================

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ==========================================================
    # CONTEXT GENERATION
    # ==========================================================

    selected_tables: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    business_knowledge: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    join_knowledge: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    forbidden_joins: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    semantic_context: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sql_patterns: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    full_context: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # PROMPT
    # ==========================================================

    prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # SQL GENERATION
    # ==========================================================

    generated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    validated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # SQL RESULT
    # ==========================================================

    sql_result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    formatted_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # EXECUTION
    # ==========================================================

    execution_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="SUCCESS",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )