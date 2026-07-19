from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class FactPrixIndices(Base):

    __tablename__ = "FACT_PRIX_INDICES"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    niveau_geo: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    id_region: Mapped[int | None] = mapped_column(
        ForeignKey("REGION.id_region"),
        nullable=True,
    )

    id_province: Mapped[int | None] = mapped_column(
        ForeignKey("PROVINCE_PREFECTURE.id_province"),
        nullable=True,
    )

    id_niveau_mat: Mapped[int] = mapped_column(
        ForeignKey("NIVEAU_MATERIAU.id"),
        nullable=False,
    )

    annee: Mapped[int] = mapped_column(
        ForeignKey("DIM_TEMPS.annee"),
        nullable=False,
    )

    prix_moyen: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    indice: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    type_fichier: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    code_csv_source: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    date_chargement: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    region: Mapped["Region | None"] = relationship(
        "Region",
        back_populates="prix_indices",
    )

    province: Mapped["ProvincePrefecture | None"] = relationship(
        "ProvincePrefecture",
        back_populates="prix_indices",
    )

    niveau_materiau: Mapped["NiveauMateriau"] = relationship(
        "NiveauMateriau",
        back_populates="prix_indices",
    )

    periode: Mapped["DimTemps"] = relationship(
        "DimTemps",
        back_populates="prix_indices",
    )