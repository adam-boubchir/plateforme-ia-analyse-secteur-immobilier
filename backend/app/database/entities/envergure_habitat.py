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


class EnvergureHabitat(Base):

    __tablename__ = "ENVERGURE_HABITAT"

    id_envergure: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code_envergure: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        unique=True,
    )

    nom_envergure: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    indicateurs_habitat: Mapped[list["FactIndicateurHabitat"]] = relationship(
        "FactIndicateurHabitat",
        back_populates="envergure",
    )