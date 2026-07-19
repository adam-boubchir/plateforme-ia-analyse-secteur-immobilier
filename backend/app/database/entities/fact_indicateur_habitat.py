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


class FactIndicateurHabitat(Base):

    __tablename__ = "FACT_INDICATEUR_HABITAT"

    id_fact: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    niveau_geo: Mapped[str] = mapped_column(
        String(20),
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

    id_type_habitat: Mapped[int] = mapped_column(
        ForeignKey("TYPE_HABITAT.id_type_habitat"),
        nullable=False,
    )

    id_envergure: Mapped[int | None] = mapped_column(
        ForeignKey("ENVERGURE_HABITAT.id_envergure"),
        nullable=True,
    )

    annee: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    type_indicateur: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    montant_mad: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )

    indice: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
    )

    date_chargement: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    region: Mapped["Region | None"] = relationship(
        "Region",
        back_populates="indicateurs_habitat",
    )

    province: Mapped["ProvincePrefecture | None"] = relationship(
        "ProvincePrefecture",
        back_populates="indicateurs_habitat",
    )

    type_habitat: Mapped["TypeHabitat"] = relationship(
        "TypeHabitat",
        back_populates="indicateurs_habitat",
    )

    envergure: Mapped["EnvergureHabitat | None"] = relationship(
        "EnvergureHabitat",
        back_populates="indicateurs_habitat",
    )