from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class DimTemps(Base):

    __tablename__ = "DIM_TEMPS"

    annee: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    prix_indices: Mapped[list["FactPrixIndices"]] = relationship(
        "FactPrixIndices",
        back_populates="periode",
    )