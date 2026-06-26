from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Integer,
    Numeric,
    Boolean,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from .base import Base


class ModelConfigEntity(Base):

    __tablename__ = "model_config"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    agent_name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    provider: Mapped[str] = mapped_column(
        String(50)
    )

    model_name: Mapped[str] = mapped_column(
        String(100)
    )

    api_key_alias: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    api_base_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    deployment_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    system_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    temperature: Mapped[Decimal] = mapped_column(
        Numeric(3, 2)
    )

    top_p: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=1.00
    )

    frequency_penalty: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=0.00
    )

    presence_penalty: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=0.00
    )

    timeout_seconds: Mapped[int] = mapped_column(
        Integer,
        default=60
    )

    max_tokens: Mapped[int] = mapped_column(
        Integer
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )