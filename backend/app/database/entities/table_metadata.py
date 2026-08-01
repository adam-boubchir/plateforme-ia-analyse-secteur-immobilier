from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func

from .base import Base


class TableMetadataEntity(Base):
    """
    ORM entity representing metadata of one database table.
    """

    __tablename__ = "table_metadata"

    # ==========================================================
    # IDENTIFIERS
    # ==========================================================

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================================
    # TABLE INFORMATION
    # ==========================================================

    source_database: Mapped[str] = mapped_column(
        String(255),
    )

    schema_name: Mapped[str] = mapped_column(
        String(255),
    )

    table_name: Mapped[str] = mapped_column(
        String(255),
    )

    table_type: Mapped[str] = mapped_column(
        String(50),
    )

    # ==========================================================
    # BUSINESS INFORMATION
    # ==========================================================

    business_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # METADATA
    # ==========================================================

    row_count: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    is_fact_table: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    last_refresh: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=func.now(),
    )


__all__ = [
    "TableMetadataEntity",
]