from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class Region(Base):

    __tablename__ = "REGION"

    id_region: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code_region: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    nom_region: Mapped[str] = mapped_column(
        String(400),
        nullable=False,
    )

    nom_region_ar: Mapped[str | None] = mapped_column(
        String(400),
        nullable=True,
    )

    code_iso: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    provinces: Mapped[list["ProvincePrefecture"]] = relationship(
        "ProvincePrefecture",
        back_populates="region",
    )

    indicateurs_habitat: Mapped[list["FactIndicateurHabitat"]] = relationship(
        "FactIndicateurHabitat",
        back_populates="region",
    )

    prix_indices: Mapped[list["FactPrixIndices"]] = relationship(
        "FactPrixIndices",
        back_populates="region",
    )