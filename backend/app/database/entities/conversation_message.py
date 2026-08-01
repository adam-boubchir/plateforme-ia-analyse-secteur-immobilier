from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class ConversationMessage(Base):
    """
    ORM entity representing one message exchanged
    during a conversation.

    A message can originate from a user or from an AI agent.
    """

    __tablename__ = "conversation_messages"

    # ==========================================================
    # IDENTIFICATION
    # ==========================================================

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    request_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    # ==========================================================
    # MESSAGE
    # ==========================================================

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ==========================================================
    # SQL EXECUTION
    # ==========================================================

    generated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    result_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    execution_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    rows_returned: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ==========================================================
    # STATUS
    # ==========================================================

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # ==========================================================
    # TIMESTAMP
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # ==========================================================
    # RELATIONSHIP
    # ==========================================================

    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )


__all__ = [
    "ConversationMessage",
]