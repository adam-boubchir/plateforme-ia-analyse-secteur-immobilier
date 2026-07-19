from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class ProvincePrefecture(Base):

    __tablename__ = "PROVINCE_PREFECTURE"

    id_province: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code_province: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    nom_province: Mapped[str] = mapped_column(
        String(400),
        nullable=False,
    )

    nom_province_ar: Mapped[str | None] = mapped_column(
        String(400),
        nullable=True,
    )

    code_iso: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    id_region: Mapped[int | None] = mapped_column(
        ForeignKey("REGION.id_region"),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    region: Mapped["Region | None"] = relationship(
        "Region",
        back_populates="provinces",
    )

    indicateurs_habitat: Mapped[list["FactIndicateurHabitat"]] = relationship(
        "FactIndicateurHabitat",
        back_populates="province",
    )

    prix_indices: Mapped[list["FactPrixIndices"]] = relationship(
        "FactPrixIndices",
        back_populates="province",
    )