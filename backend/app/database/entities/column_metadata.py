from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Boolean,
    Text,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class ColumnMetadataEntity(Base):

    __tablename__ = "column_metadata"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    table_id: Mapped[int] = mapped_column(
        ForeignKey("table_metadata.id")
    )

    table_name: Mapped[str] = mapped_column(
        String(255)
    )

    column_name: Mapped[str] = mapped_column(
        String(255)
    )

    business_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    data_type: Mapped[str] = mapped_column(
        String(100)
    )

    is_nullable: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_primary_key: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_foreign_key: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    sample_values: Mapped[str | None] = mapped_column(
        Text,
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