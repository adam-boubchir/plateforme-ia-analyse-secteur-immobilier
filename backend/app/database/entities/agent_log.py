from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Integer,
    Text
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class AgentLogEntity(Base):

    __tablename__ = "agent_logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    request_id: Mapped[str] = mapped_column(
        String(100)
    )

    timestamp_utc: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    agent_name: Mapped[str] = mapped_column(
        String(100)
    )

    model_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    user_question: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    generated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    execution_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    rows_returned: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )