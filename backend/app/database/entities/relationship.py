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


class RelationshipEntity(Base):

    __tablename__ = "relationships"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    constraint_name: Mapped[str] = mapped_column(
        String(255)
    )

    source_schema: Mapped[str] = mapped_column(
        String(255)
    )

    source_table: Mapped[str] = mapped_column(
        String(255)
    )

    source_column: Mapped[str] = mapped_column(
        String(255)
    )

    target_schema: Mapped[str] = mapped_column(
        String(255)
    )

    target_table: Mapped[str] = mapped_column(
        String(255)
    )

    target_column: Mapped[str] = mapped_column(
        String(255)
    )

    relationship_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
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