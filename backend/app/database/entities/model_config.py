from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy.sql import func

from .base import Base


class ModelConfigEntity(Base):
    """
    Configuration stored in the database for an AI agent.
    """

    __tablename__ = "model_config"

    # ==========================================================
    # IDENTIFICATION
    # ==========================================================

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    agent_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    # ==========================================================
    # MODEL
    # ==========================================================

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    deployment_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ==========================================================
    # API
    # ==========================================================

    api_key_alias: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    api_base_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ==========================================================
    # PROMPT
    # ==========================================================

    system_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # MODEL PARAMETERS
    # ==========================================================

    temperature: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        nullable=False,
    )

    top_p: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=Decimal("1.00"),
        nullable=False,
    )

    frequency_penalty: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    presence_penalty: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    timeout_seconds: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    max_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # ==========================================================
    # STATUS
    # ==========================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )