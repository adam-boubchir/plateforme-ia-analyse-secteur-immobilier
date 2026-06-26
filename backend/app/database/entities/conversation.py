from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    conversation_id: Mapped[str] = mapped_column(
        String(100)
    )

    request_id: Mapped[str] = mapped_column(
        String(100)
    )

    user_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    agent_name: Mapped[str] = mapped_column(
        String(100)
    )

    user_message: Mapped[str] = mapped_column(
        Text
    )

    assistant_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )

    created_at: Mapped[str] = mapped_column(
        DateTime
    )