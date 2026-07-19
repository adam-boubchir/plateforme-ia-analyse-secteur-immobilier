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


class NiveauMateriau(Base):

    __tablename__ = "NIVEAU_MATERIAU"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nom: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    niveau: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    id_parent: Mapped[int | None] = mapped_column(
        ForeignKey("NIVEAU_MATERIAU.id"),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    parent: Mapped["NiveauMateriau | None"] = relationship(
        "NiveauMateriau",
        remote_side=[id],
        back_populates="enfants",
    )

    enfants: Mapped[list["NiveauMateriau"]] = relationship(
        "NiveauMateriau",
        back_populates="parent",
    )

    prix_indices: Mapped[list["FactPrixIndices"]] = relationship(
        "FactPrixIndices",
        back_populates="niveau_materiau",
    )