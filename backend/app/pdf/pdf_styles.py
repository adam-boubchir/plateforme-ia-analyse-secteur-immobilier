from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_JUSTIFY,
    TA_LEFT,
)
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm

__all__ = (
    "PDFStyles",
)


class PDFStyles:
    """
    Centralized visual identity for every generated PDF.

    All colors, fonts, margins and paragraph styles
    are defined here.

    Future changes to the design should only require
    editing this file.
    """

    # ======================================================
    # PAGE
    # ======================================================

    PAGE_MARGIN_LEFT = 2.2 * cm
    PAGE_MARGIN_RIGHT = 2.2 * cm

    PAGE_MARGIN_TOP = 2.8 * cm
    PAGE_MARGIN_BOTTOM = 2.3 * cm

    # ======================================================
    # COLORS
    # ======================================================

    PRIMARY = colors.HexColor("#0B3D6E")

    SECONDARY = colors.HexColor("#3B82F6")

    ACCENT = colors.HexColor("#14B8A6")

    SUCCESS = colors.HexColor("#16A34A")

    WARNING = colors.HexColor("#F59E0B")

    DANGER = colors.HexColor("#DC2626")

    TITLE = colors.HexColor("#111827")

    TEXT = colors.HexColor("#374151")

    SUBTITLE = colors.HexColor("#6B7280")

    BORDER = colors.HexColor("#D1D5DB")

    TABLE_HEADER = colors.HexColor("#E5E7EB")

    TABLE_ROW = colors.HexColor("#F9FAFB")

    WHITE = colors.white

    BLACK = colors.black

    GREY = colors.HexColor("#808080")

    LIGHT_GREY = colors.HexColor("#DADADA")

    # ======================================================
    # TYPOGRAPHY
    # ======================================================

    FONT = "Helvetica"

    FONT_BOLD = "Helvetica-Bold"

    FONT_ITALIC = "Helvetica-Oblique"

    # ======================================================
    # BASE
    # ======================================================

    _styles = getSampleStyleSheet()

    # ======================================================
    # COVER TITLE
    # ======================================================

    COVER_TITLE = ParagraphStyle(
        "CoverTitle",
        parent=_styles["Title"],
        fontName=FONT_BOLD,
        fontSize=30,
        leading=36,
        alignment=TA_CENTER,
        textColor=PRIMARY,
        spaceAfter=22,
    )

    # ======================================================
    # COVER SUBTITLE
    # ======================================================

    COVER_SUBTITLE = ParagraphStyle(
        "CoverSubtitle",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=14,
        leading=20,
        alignment=TA_CENTER,
        textColor=SUBTITLE,
        spaceAfter=30,
    )

    # ======================================================
    # H1
    # ======================================================

    HEADING_1 = ParagraphStyle(
        "Heading1",
        parent=_styles["Heading1"],
        fontName=FONT_BOLD,
        fontSize=20,
        leading=26,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=14,
    )

    # ======================================================
    # H2
    # ======================================================

    HEADING_2 = ParagraphStyle(
        "Heading2",
        parent=_styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=16,
        leading=22,
        textColor=SECONDARY,
        spaceBefore=16,
        spaceAfter=10,
    )

    # ======================================================
    # H3
    # ======================================================

    HEADING_3 = ParagraphStyle(
        "Heading3",
        parent=_styles["Heading3"],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=18,
        textColor=TITLE,
        spaceBefore=14,
        spaceAfter=8,
    )

    # ======================================================
    # BODY
    # ======================================================

    BODY = ParagraphStyle(
        "Body",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=10.5,
        leading=18,
        alignment=TA_JUSTIFY,
        textColor=TEXT,
        spaceAfter=10,
    )

    # ======================================================
    # SMALL
    # ======================================================

    SMALL = ParagraphStyle(
        "Small",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=9,
        leading=12,
        textColor=SUBTITLE,
    )

    # ======================================================
    # FOOTER
    # ======================================================

    FOOTER = ParagraphStyle(
        "Footer",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=SUBTITLE,
    )

    # ======================================================
    # TABLE TITLE
    # ======================================================

    TABLE_TITLE = ParagraphStyle(
        "TableTitle",
        parent=_styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=12,
        textColor=TITLE,
        alignment=TA_LEFT,
        spaceAfter=8,
    )

    # ======================================================
    # CAPTION
    # ======================================================

    CAPTION = ParagraphStyle(
        "Caption",
        parent=_styles["BodyText"],
        fontName=FONT_ITALIC,
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=SUBTITLE,
        spaceBefore=6,
    )

    SECTION_NUMBER = ParagraphStyle(

        "SectionNumber",

        parent=_styles["Heading1"],

        fontName=FONT_BOLD,

        fontSize=18,

        leading=24,

        textColor=PRIMARY,

        spaceBefore=22,

        spaceAfter=14,

    )

    SQL = ParagraphStyle(

        "SQL",

        parent=_styles["Code"],

        fontName="Courier",

        fontSize=9,

        leading=13,

        textColor=colors.HexColor("#1F2937"),

    )

    INFO = ParagraphStyle(

        "Info",

        parent=_styles["BodyText"],

        fontName=FONT,

        fontSize=9,

        leading=12,

        textColor=SUBTITLE,

        leftIndent=12,

    )

        # ======================================================
    # KPI
    # ======================================================

    KPI_VALUE = ParagraphStyle(
        "KPIValue",
        parent=_styles["BodyText"],
        fontName=FONT_BOLD,
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=PRIMARY,
    )

    KPI_LABEL = ParagraphStyle(
        "KPILabel",
        parent=_styles["BodyText"],
        fontName=FONT_BOLD,
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=SUBTITLE,
    )

    KPI_DESCRIPTION = ParagraphStyle(
        "KPIDescription",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=SUBTITLE,
    )

    # ======================================================
    # REPORT INFO
    # ======================================================

    REPORT_INFO = ParagraphStyle(
        "ReportInfo",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=9,
        leading=13,
        textColor=TEXT,
        spaceAfter=4,
    )

    # ======================================================
    # TABLE CELL
    # ======================================================

    TABLE_CELL = ParagraphStyle(
        "TableCell",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        textColor=TEXT,
    )

    TABLE_CELL_CENTER = ParagraphStyle(
        "TableCellCenter",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=TEXT,
    )

    # ======================================================
    # INSIGHT
    # ======================================================

    INSIGHT = ParagraphStyle(
        "Insight",
        parent=_styles["BodyText"],
        fontName=FONT,
        fontSize=10,
        leading=15,
        textColor=TEXT,
        leftIndent=10,
        rightIndent=10,
        spaceAfter=6,
    )