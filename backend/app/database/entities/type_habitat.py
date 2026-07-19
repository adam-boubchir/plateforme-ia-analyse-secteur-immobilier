from __future__ import annotations

from sqlalchemy import (
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class TypeHabitat(Base):

    __tablename__ = "TYPE_HABITAT"

    id_type_habitat: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )

    nom_type: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    indicateurs_habitat: Mapped[list["FactIndicateurHabitat"]] = relationship(
        "FactIndicateurHabitat",
        back_populates="type_habitat",
    )