from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Boolean,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from .base import Base


class TableMetadataEntity(Base):

    __tablename__ = "table_metadata"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    source_database: Mapped[str] = mapped_column(
        String(255)
    )

    schema_name: Mapped[str] = mapped_column(
        String(255)
    )

    table_name: Mapped[str] = mapped_column(
        String(255)
    )

    table_type: Mapped[str] = mapped_column(
        String(50)
    )

    business_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    row_count: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    is_fact_table: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    last_refresh: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )