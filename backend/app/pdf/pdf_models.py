from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime


__all__ = (
    "PDFMetadata",
    "PDFKPI",
    "PDFSection",
    "PDFTable",
    "PDFImage",
    "PDFDocument",
)


# ==========================================================
# METADATA
# ==========================================================


@dataclass(slots=True)
class PDFMetadata:
    """
    Metadata embedded inside the generated PDF.
    """

    title: str

    author: str

    subject: str

    keywords: list[str] = field(
        default_factory=list,
    )

    creator: str = (
        "Plateforme IA d'Analyse du Secteur Immobilier"
    )

    producer: str = (
        "Immobilier AI PDF Engine"
    )


# ==========================================================
# KPI
# ==========================================================


@dataclass(slots=True)
class PDFKPI:
    """
    Key performance indicator displayed
    as a visual card inside the report.
    """

    label: str

    value: str

    description: str | None = None

    unit: str | None = None


# ==========================================================
# SECTIONS
# ==========================================================


@dataclass(slots=True)
class PDFSection:
    """
    One analytical section of the report.
    """

    title: str

    content: str

    level: int = 1


# ==========================================================
# TABLES
# ==========================================================


@dataclass(slots=True)
class PDFTable:
    """
    Table displayed inside the report.
    """

    title: str

    headers: list[str]

    rows: list[list[str]]

    max_rows: int | None = None

    caption: str | None = None


# ==========================================================
# IMAGES / CHARTS
# ==========================================================


@dataclass(slots=True)
class PDFImage:
    """
    Chart or image inserted inside the report.
    """

    path: str

    caption: str | None = None

    title: str | None = None

    width: int | None = None

    height: int | None = None

    keep_aspect_ratio: bool = True

    page_break_before: bool = False

    page_break_after: bool = False


# ==========================================================
# DOCUMENT
# ==========================================================


@dataclass(slots=True)
class PDFDocument:
    """
    Complete document model used by the PDF engine.
    """

    # ------------------------------------------------------
    # COVER
    # ------------------------------------------------------

    title: str

    subtitle: str

    author: str

    # ------------------------------------------------------
    # MAIN QUESTION
    # ------------------------------------------------------

    content: str

    # ------------------------------------------------------
    # ANALYTICAL CONTENT
    # ------------------------------------------------------

    sections: list[PDFSection] = field(
        default_factory=list,
    )

    # ------------------------------------------------------
    # KEY PERFORMANCE INDICATORS
    # ------------------------------------------------------

    kpis: list[PDFKPI] = field(
        default_factory=list,
    )

    # ------------------------------------------------------
    # TABLES
    # ------------------------------------------------------

    tables: list[PDFTable] = field(
        default_factory=list,
    )

    # ------------------------------------------------------
    # VISUALIZATIONS
    # ------------------------------------------------------

    images: list[PDFImage] = field(
        default_factory=list,
    )

    # ------------------------------------------------------
    # INSIGHTS
    # ------------------------------------------------------

    insights: list[str] = field(
        default_factory=list,
    )

    # ------------------------------------------------------
    # METADATA
    # ------------------------------------------------------

    metadata: PDFMetadata | None = None

    # ------------------------------------------------------
    # GENERATION
    # ------------------------------------------------------

    filename: str | None = None

    created_at: datetime = field(
        default_factory=datetime.now,
    )