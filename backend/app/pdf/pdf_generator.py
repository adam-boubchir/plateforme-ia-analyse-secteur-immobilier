from __future__ import annotations

import html
import re

from pathlib import Path
from uuid import uuid4

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    NextPageTemplate,
    Table,
    TableStyle,
    KeepTogether,
)

from app.pdf.pdf_models import PDFDocument
from app.pdf.pdf_styles import PDFStyles
from app.storage.storage_service import StorageService


__all__ = (
    "PDFGenerator",
)


class PDFGenerator:
    """
    Professional PDF generator for Immobilier IA.

    Responsibilities
    ----------------
    - Generate the report cover.
    - Generate report information.
    - Convert Markdown-like AI responses into readable PDF elements.
    - Generate structured sections.
    - Generate readable SQL blocks.
    - Generate responsive tables.
    - Generate charts and visualizations.
    - Generate KPI cards.
    - Generate headers and footers.
    - Save the final PDF through StorageService.
    """

    def __init__(
        self,
        *,
        storage_service: StorageService,
    ) -> None:

        self._storage = storage_service

    # ==========================================================
    # PATHS
    # ==========================================================

    def _header_image_path(self) -> Path:
        """
        Return the institutional header image.
        """

        return (
            Path(__file__)
            .resolve()
            .parents[2]
            / "assets"
            / "reports"
            / "ministry_header.png"
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        document: PDFDocument,
    ) -> str:
        """
        Generate the complete PDF report.

        Parameters
        ----------
        document:
            Structured PDF document.

        Returns
        -------
        str
            Saved PDF path.
        """

        filename = f"{uuid4().hex}.pdf"

        temp_path = (
            Path("storage")
            / filename
        )

        temp_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        doc = self._create_document(
            output_path=temp_path,
        )

        story: list = []

        # ------------------------------------------------------
        # COVER
        # ------------------------------------------------------

        self._build_cover(
            story=story,
            document=document,
        )

        # ------------------------------------------------------
        # TABLE OF CONTENTS
        # ------------------------------------------------------

        self._build_table_of_contents(
            story=story,
            document=document,
        )

        # ------------------------------------------------------
        # REPORT INFORMATION
        # ------------------------------------------------------

        self._build_report_information(
            story=story,
            document=document,
        )

        # ------------------------------------------------------
        # MAIN CONTENT
        # ------------------------------------------------------

        self._build_content(
            story=story,
            document=document,
        )

        # ------------------------------------------------------
        # BUILD PDF
        # ------------------------------------------------------

        doc.build(
            story,
        )

        # ------------------------------------------------------
        # SAVE
        # ------------------------------------------------------

        saved_path = self._storage.save_report(
            str(temp_path),
        )

        print("=" * 80)
        print("PDF GENERATOR")
        print("TEMP PATH  :", temp_path)
        print("SAVED PATH :", saved_path)
        print("=" * 80)

        temp_path.unlink(
            missing_ok=True,
        )

        return saved_path

    # ==========================================================
    # DOCUMENT
    # ==========================================================

    def _create_document(
        self,
        *,
        output_path: Path,
    ) -> BaseDocTemplate:
        """
        Create the ReportLab document.
        """

        page_width, page_height = A4

        frame_width = (
            page_width
            - PDFStyles.PAGE_MARGIN_LEFT
            - PDFStyles.PAGE_MARGIN_RIGHT
        )

        frame_height = (
            page_height
            - PDFStyles.PAGE_MARGIN_TOP
            - PDFStyles.PAGE_MARGIN_BOTTOM
        )

        normal_frame = Frame(
            PDFStyles.PAGE_MARGIN_LEFT,
            PDFStyles.PAGE_MARGIN_BOTTOM,
            frame_width,
            frame_height,
            id="normal",
        )

        cover_frame = Frame(
            PDFStyles.PAGE_MARGIN_LEFT,
            PDFStyles.PAGE_MARGIN_BOTTOM,
            frame_width,
            frame_height,
            id="cover",
        )

        cover_template = PageTemplate(
            id="cover",
            frames=[cover_frame],
            onPage=self._draw_cover,
        )

        normal_template = PageTemplate(
            id="normal",
            frames=[normal_frame],
            onPage=self._draw_page,
        )

        return BaseDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=PDFStyles.PAGE_MARGIN_LEFT,
            rightMargin=PDFStyles.PAGE_MARGIN_RIGHT,
            topMargin=PDFStyles.PAGE_MARGIN_TOP,
            bottomMargin=PDFStyles.PAGE_MARGIN_BOTTOM,
            pageTemplates=[
                cover_template,
                normal_template,
            ],
        )

    # ==========================================================
    # COVER
    # ==========================================================

    def _build_cover(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Build the professional cover page.
        """

        story.append(
            Spacer(
                1,
                1.5 * cm,
            )
        )

        # ------------------------------------------------------
        # INSTITUTIONAL HEADER
        # ------------------------------------------------------

        header_path = self._header_image_path()

        if header_path.exists():

            header = Image(
                str(header_path),
            )

            header.drawWidth = 17 * cm
            header.drawHeight = 3 * cm
            header.hAlign = "CENTER"

            story.append(header)

        story.append(
            Spacer(
                1,
                2.5 * cm,
            )
        )

        # ------------------------------------------------------
        # REPORT LABEL
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "RAPPORT D'ANALYSE",
                PDFStyles.COVER_TITLE,
            )
        )

        story.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        story.append(
            Paragraph(
                self._escape(document.title),
                PDFStyles.COVER_TITLE,
            )
        )

        story.append(
            Spacer(
                1,
                0.6 * cm,
            )
        )

        # ------------------------------------------------------
        # SUBTITLE
        # ------------------------------------------------------

        story.append(
            Paragraph(
                self._escape(document.subtitle),
                PDFStyles.COVER_SUBTITLE,
            )
        )

        story.append(
            Spacer(
                1,
                2.5 * cm,
            )
        )

        # ------------------------------------------------------
        # INFORMATION CARD
        # ------------------------------------------------------

        cover_information = [
            [
                Paragraph(
                    "<b>Organisme</b>",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    self._escape(document.author),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "<b>Date de génération</b>",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    document.created_at.strftime(
                        "%d/%m/%Y à %H:%M"
                    ),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "<b>Plateforme</b>",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    "Immobilier IA",
                    PDFStyles.TABLE_CELL,
                ),
            ],
        ]

        information_table = Table(
            cover_information,
            colWidths=[
                5 * cm,
                10 * cm,
            ],
        )

        information_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        PDFStyles.TABLE_HEADER,
                    ),
                    (
                        "BACKGROUND",
                        (1, 0),
                        (1, -1),
                        PDFStyles.TABLE_ROW,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.7,
                        PDFStyles.BORDER,
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.3,
                        PDFStyles.BORDER,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                ]
            )
        )

        story.append(
            information_table
        )

        # ------------------------------------------------------
        # SWITCH TO NORMAL TEMPLATE
        # ------------------------------------------------------

        story.append(
            NextPageTemplate("normal")
        )

        story.append(
            PageBreak()
        )

    # ==========================================================
    # TABLE OF CONTENTS
    # ==========================================================

    def _build_table_of_contents(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Build a clean table of contents.

        Note:
        This is a structural TOC, not a dynamically numbered
        ReportLab TableOfContents.
        """

        story.append(
            Paragraph(
                "SOMMAIRE",
                PDFStyles.HEADING_1,
            )
        )

        story.append(
            Spacer(
                1,
                0.4 * cm,
            )
        )

        story.append(
            Paragraph(
                "Structure du rapport",
                PDFStyles.BODY,
            )
        )

        story.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

        items: list[str] = []

        items.append(
            "1. Objet de la demande"
        )

        number = 2

        for section in document.sections:

            items.append(
                f"{number}. "
                f"{self._escape(section.title)}"
            )

            number += 1

        if document.tables:

            items.append(
                f"{number}. Résultats SQL"
            )

            number += 1

        if document.images:

            items.append(
                f"{number}. Visualisations"
            )

            number += 1

        items.append(
            f"{number}. Conclusion"
        )

        for item in items:

            story.append(
                Paragraph(
                    f"• {item}",
                    PDFStyles.BODY,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.08 * cm,
                )
            )

        story.append(
            PageBreak()
        )

    # ==========================================================
    # REPORT INFORMATION
    # ==========================================================

    def _build_report_information(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Build the report metadata page.
        """

        story.append(
            Paragraph(
                "INFORMATIONS DU RAPPORT",
                PDFStyles.HEADING_1,
            )
        )

        story.append(
            Spacer(
                1,
                0.3 * cm,
            )
        )

        story.append(
            Paragraph(
                (
                    "Cette page présente les principales "
                    "informations relatives au rapport généré "
                    "automatiquement par Immobilier IA."
                ),
                PDFStyles.BODY,
            )
        )

        story.append(
            Spacer(
                1,
                0.6 * cm,
            )
        )

        rows_count = 0
        columns_count = 0

        if document.tables:

            rows_count = len(
                document.tables[0].rows
            )

            columns_count = len(
                document.tables[0].headers
            )

        information_data = [
            [
                Paragraph(
                    "Champ",
                    PDFStyles.TABLE_CELL_CENTER,
                ),
                Paragraph(
                    "Valeur",
                    PDFStyles.TABLE_CELL_CENTER,
                ),
            ],
            [
                Paragraph(
                    "Titre du rapport",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    self._escape(document.title),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Sous-titre",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    self._escape(document.subtitle),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Auteur",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    self._escape(document.author),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Date de génération",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    document.created_at.strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Nombre de sections",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    str(len(document.sections)),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Nombre de tableaux",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    str(len(document.tables)),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Nombre de graphiques",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    str(len(document.images)),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Lignes SQL",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    str(rows_count),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Colonnes SQL",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    str(columns_count),
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Source des données",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    "SQL Server - Ministère de l'Habitat",
                    PDFStyles.TABLE_CELL,
                ),
            ],
            [
                Paragraph(
                    "Plateforme",
                    PDFStyles.TABLE_CELL,
                ),
                Paragraph(
                    "Immobilier IA",
                    PDFStyles.TABLE_CELL,
                ),
            ],
        ]

        info_table = Table(
            information_data,
            colWidths=[
                5.5 * cm,
                10.5 * cm,
            ],
            repeatRows=1,
        )

        info_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        PDFStyles.PRIMARY,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        PDFStyles.WHITE,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        PDFStyles.TABLE_ROW,
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            PDFStyles.TABLE_ROW,
                            PDFStyles.WHITE,
                        ],
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        PDFStyles.BORDER,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            )
        )

        story.append(
            info_table
        )

        story.append(
            Spacer(
                1,
                0.8 * cm,
            )
        )

        story.append(
            Paragraph(
                (
                    "Les informations ci-dessus sont générées "
                    "automatiquement au moment de la création "
                    "du rapport afin d'assurer la traçabilité "
                    "et la compréhension du document."
                ),
                PDFStyles.BODY,
            )
        )

        story.append(
            PageBreak()
        )

    # ==========================================================
    # MAIN CONTENT
    # ==========================================================

    def _build_content(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Build the complete analytical report.
        """

        # ======================================================
        # REQUEST
        # ======================================================

        story.append(
            Paragraph(
                "1. Objet de la demande",
                PDFStyles.HEADING_1,
            )
        )

        story.append(
            Spacer(
                1,
                0.2 * cm,
            )
        )

        self._append_markdown(
            story=story,
            text=document.content,
        )

        # ======================================================
        # KPIs
        # ======================================================

        if document.kpis:

            story.append(
                Spacer(
                    1,
                    0.4 * cm,
                )
            )

            story.append(
                Paragraph(
                    "Indicateurs clés",
                    PDFStyles.HEADING_2,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.2 * cm,
                )
            )

            self._build_kpis(
                story=story,
                document=document,
            )

        # ======================================================
        # ANALYTICAL SECTIONS
        # ======================================================

        section_number = 2

        for section in document.sections:

            story.append(
                Spacer(
                    1,
                    0.3 * cm,
                )
            )

            story.append(
                Paragraph(
                    (
                        f"{section_number}. "
                        f"{self._escape(section.title)}"
                    ),
                    PDFStyles.HEADING_1,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.1 * cm,
                )
            )

            self._append_markdown(
                story=story,
                text=section.content,
            )

            section_number += 1

        # ======================================================
        # SQL RESULTS
        # ======================================================

        for table in document.tables:

            story.append(
                Spacer(
                    1,
                    0.5 * cm,
                )
            )

            story.append(
                Paragraph(
                    (
                        f"{section_number}. "
                        f"{self._escape(table.title)}"
                    ),
                    PDFStyles.HEADING_1,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.25 * cm,
                )
            )

            self._build_results_table(
                story=story,
                table=table,
            )

            section_number += 1

        # ======================================================
        # VISUALIZATIONS
        # ======================================================

        if document.images:

            story.append(
                PageBreak()
            )

            story.append(
                Paragraph(
                    (
                        f"{section_number}. "
                        "Visualisations"
                    ),
                    PDFStyles.HEADING_1,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.2 * cm,
                )
            )

            story.append(
                Paragraph(
                    (
                        "Les visualisations suivantes présentent "
                        "les tendances et comparaisons principales "
                        "identifiées à partir des résultats."
                    ),
                    PDFStyles.BODY,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.3 * cm,
                )
            )

            self._build_images(
                story=story,
                document=document,
            )

    # ==========================================================
    # MARKDOWN
    # ==========================================================

    def _append_markdown(
        self,
        *,
        story: list,
        text: str | None,
    ) -> None:
        """
        Convert a lightweight Markdown response into
        readable ReportLab flowables.

        Supported syntax:
        - # Heading
        - ## Heading
        - ### Heading
        - bullet lists
        - numbered lists
        - bold text
        - italic text
        - inline code
        - code blocks
        - normal paragraphs
        """

        if not text:
            return

        normalized = text.replace(
            "\r\n",
            "\n",
        ).replace(
            "\r",
            "\n",
        )

        lines = normalized.split("\n")

        paragraph_lines: list[str] = []
        code_lines: list[str] = []
        in_code_block = False

        def flush_paragraph() -> None:

            if not paragraph_lines:
                return

            content = " ".join(
                line.strip()
                for line in paragraph_lines
                if line.strip()
            ).strip()

            paragraph_lines.clear()

            if not content:
                return

            story.append(
                Paragraph(
                    self._markdown_inline(content),
                    PDFStyles.BODY,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.12 * cm,
                )
            )

        def flush_code() -> None:

            if not code_lines:
                return

            code = "\n".join(
                code_lines
            )

            code_lines.clear()

            story.append(
                self._build_code_block(
                    code,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.25 * cm,
                )
            )

        for raw_line in lines:

            line = raw_line.strip()

            # --------------------------------------------------
            # CODE BLOCK
            # --------------------------------------------------

            if line.startswith("```"):

                flush_paragraph()

                if in_code_block:

                    flush_code()

                    in_code_block = False

                else:

                    in_code_block = True

                continue

            if in_code_block:

                code_lines.append(
                    raw_line
                )

                continue

            # --------------------------------------------------
            # EMPTY LINE
            # --------------------------------------------------

            if not line:

                flush_paragraph()

                continue

            # --------------------------------------------------
            # H1
            # --------------------------------------------------

            match = re.match(
                r"^#\s+(.+)$",
                line,
            )

            if match:

                flush_paragraph()

                story.append(
                    Paragraph(
                        self._markdown_inline(
                            match.group(1)
                        ),
                        PDFStyles.HEADING_1,
                    )
                )

                continue

            # --------------------------------------------------
            # H2
            # --------------------------------------------------

            match = re.match(
                r"^##\s+(.+)$",
                line,
            )

            if match:

                flush_paragraph()

                story.append(
                    Paragraph(
                        self._markdown_inline(
                            match.group(1)
                        ),
                        PDFStyles.HEADING_2,
                    )
                )

                continue

            # --------------------------------------------------
            # H3
            # --------------------------------------------------

            match = re.match(
                r"^###\s+(.+)$",
                line,
            )

            if match:

                flush_paragraph()

                story.append(
                    Paragraph(
                        self._markdown_inline(
                            match.group(1)
                        ),
                        PDFStyles.HEADING_3,
                    )
                )

                continue

            # --------------------------------------------------
            # BULLET
            # --------------------------------------------------

            match = re.match(
                r"^[-*]\s+(.+)$",
                line,
            )

            if match:

                flush_paragraph()

                story.append(
                    Paragraph(
                        f"• {self._markdown_inline(match.group(1))}",
                        PDFStyles.BODY,
                    )
                )

                continue

            # --------------------------------------------------
            # NUMBERED LIST
            # --------------------------------------------------

            match = re.match(
                r"^\d+\.\s+(.+)$",
                line,
            )

            if match:

                flush_paragraph()

                story.append(
                    Paragraph(
                        self._markdown_inline(line),
                        PDFStyles.BODY,
                    )
                )

                continue

            # --------------------------------------------------
            # NORMAL TEXT
            # --------------------------------------------------

            paragraph_lines.append(
                raw_line
            )

        # ------------------------------------------------------
        # FLUSH
        # ------------------------------------------------------

        if in_code_block:

            flush_code()

        flush_paragraph()

    # ==========================================================
    # INLINE MARKDOWN
    # ==========================================================

    def _markdown_inline(
        self,
        text: str,
    ) -> str:
        """
        Convert simple inline Markdown to ReportLab markup.
        """

        text = html.escape(
            str(text),
            quote=False,
        )

        # ------------------------------------------------------
        # Inline code
        # ------------------------------------------------------

        text = re.sub(
            r"`([^`]+)`",
            r'<font name="Courier">\1</font>',
            text,
        )

        # ------------------------------------------------------
        # Bold
        # ------------------------------------------------------

        text = re.sub(
            r"\*\*(.+?)\*\*",
            r"<b>\1</b>",
            text,
        )

        # ------------------------------------------------------
        # Italic
        # ------------------------------------------------------

        text = re.sub(
            r"(?<!\*)\*([^*]+)\*(?!\*)",
            r"<i>\1</i>",
            text,
        )

        return text

    # ==========================================================
    # CODE BLOCK
    # ==========================================================

    def _build_code_block(
        self,
        code: str,
    ) -> Table:
        """
        Build a visually distinct code block.
        """

        escaped_code = html.escape(
            code,
            quote=False,
        )

        content = Paragraph(
            escaped_code.replace(
                "\n",
                "<br/>",
            ),
            PDFStyles.SQL,
        )

        code_table = Table(
            [[content]],
            colWidths=[
                A4[0]
                - PDFStyles.PAGE_MARGIN_LEFT
                - PDFStyles.PAGE_MARGIN_RIGHT
            ],
        )

        code_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor(
                            "#F3F4F6"
                        ),
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.6,
                        PDFStyles.BORDER,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                ]
            )
        )

        return code_table

    # ==========================================================
    # RESULTS TABLE
    # ==========================================================

    def _build_results_table(
        self,
        *,
        story: list,
        table,
    ) -> None:
        """
        Build a readable SQL result table.
        """

        if not table.headers:
            return

        page_width = (
            A4[0]
            - PDFStyles.PAGE_MARGIN_LEFT
            - PDFStyles.PAGE_MARGIN_RIGHT
        )

        column_count = len(
            table.headers
        )

        # ------------------------------------------------------
        # Maximum number of columns before reducing font size
        # ------------------------------------------------------

        if column_count <= 4:
            font_style = PDFStyles.TABLE_CELL

        else:
            font_style = PDFStyles.TABLE_CELL_CENTER

        data = [
            [
                Paragraph(
                    self._escape(header),
                    PDFStyles.TABLE_CELL_CENTER,
                )
                for header in table.headers
            ]
        ]

        for row in table.rows:

            formatted_row = []

            for value in row:

                if value is None:
                    value = "—"

                text = str(value)

                formatted_row.append(
                    Paragraph(
                        self._escape(text),
                        font_style,
                    )
                )

            data.append(
                formatted_row
            )

        # ------------------------------------------------------
        # Width
        # ------------------------------------------------------

        column_width = (
            page_width
            / column_count
        )

        pdf_table = Table(
            data,
            colWidths=[
                column_width
                for _ in range(column_count)
            ],
            repeatRows=1,
            splitByRow=1,
            hAlign="CENTER",
        )

        # ------------------------------------------------------
        # Style
        # ------------------------------------------------------

        pdf_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        PDFStyles.PRIMARY,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        PDFStyles.WHITE,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        PDFStyles.FONT_BOLD,
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, 0),
                        "CENTER",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        PDFStyles.BORDER,
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            PDFStyles.WHITE,
                            PDFStyles.TABLE_ROW,
                        ],
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(
            pdf_table
        )

        story.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

    # ==========================================================
    # KPI
    # ==========================================================

    def _build_kpis(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Render KPI cards.
        """

        if not document.kpis:
            return

        cards = []

        for kpi in document.kpis:

            value = str(
                kpi.value
            )

            if kpi.unit:

                value = (
                    f"{value} "
                    f"{kpi.unit}"
                )

            description = (
                kpi.description
                or ""
            )

            card_content = [
                [
                    Paragraph(
                        self._escape(kpi.label),
                        PDFStyles.KPI_LABEL,
                    )
                ],
                [
                    Paragraph(
                        self._escape(value),
                        PDFStyles.KPI_VALUE,
                    )
                ],
                [
                    Paragraph(
                        self._escape(description),
                        PDFStyles.KPI_DESCRIPTION,
                    )
                ],
            ]

            card = Table(
                card_content,
                colWidths=[
                    5.0 * cm,
                ],
            )

            card.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            PDFStyles.TABLE_ROW,
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            0.8,
                            PDFStyles.BORDER,
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE",
                        ),
                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "CENTER",
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                    ]
                )
            )

            cards.append(card)

        if not cards:
            return

        page_width = (
            A4[0]
            - PDFStyles.PAGE_MARGIN_LEFT
            - PDFStyles.PAGE_MARGIN_RIGHT
        )

        columns = min(
            len(cards),
            3,
        )

        card_width = (
            page_width / columns
        ) - 0.25 * cm

        rows = []

        for index in range(
            0,
            len(cards),
            columns,
        ):

            current = cards[
                index:index + columns
            ]

            while len(current) < columns:
                current.append("")

            rows.append(
                current
            )

        kpi_table = Table(
            rows,
            colWidths=[
                card_width
                for _ in range(columns)
            ],
            hAlign="CENTER",
        )

        kpi_table.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ]
            )
        )

        story.append(
            kpi_table
        )

    # ==========================================================
    # IMAGES
    # ==========================================================

    def _build_images(
        self,
        *,
        story: list,
        document: PDFDocument,
    ) -> None:
        """
        Render report charts and visualizations.
        """

        for index, image in enumerate(
            document.images,
            start=1,
        ):

            if image.page_break_before:

                story.append(
                    PageBreak()
                )

            image_path = Path(
                image.path
            )

            if not image_path.exists():

                story.append(
                    Paragraph(
                        "Image introuvable.",
                        PDFStyles.BODY,
                    )
                )

                continue

            # --------------------------------------------------
            # TITLE
            # --------------------------------------------------

            if image.title:

                story.append(
                    Paragraph(
                        self._escape(image.title),
                        PDFStyles.HEADING_2,
                    )
                )

            # --------------------------------------------------
            # IMAGE
            # --------------------------------------------------

            pdf_image = self._build_pdf_image(
                image_path=image_path,
            )

            story.append(
                pdf_image
            )

            # --------------------------------------------------
            # CAPTION
            # --------------------------------------------------

            if image.caption:

                story.append(
                    Spacer(
                        1,
                        0.15 * cm,
                    )
                )

                story.append(
                    Paragraph(
                        self._escape(image.caption),
                        PDFStyles.CAPTION,
                    )
                )

            story.append(
                Spacer(
                    1,
                    0.6 * cm,
                )
            )

            if image.page_break_after:

                story.append(
                    PageBreak()
                )

    # ==========================================================
    # IMAGE
    # ==========================================================

    def _build_pdf_image(
        self,
        *,
        image_path: Path,
    ) -> Image:
        """
        Fit an image inside the A4 printable area
        while preserving its aspect ratio.
        """

        pdf_image = Image(
            str(image_path)
        )

        max_width = (
            A4[0]
            - PDFStyles.PAGE_MARGIN_LEFT
            - PDFStyles.PAGE_MARGIN_RIGHT
        )

        max_height = 19 * cm

        original_width = (
            pdf_image.imageWidth
        )

        original_height = (
            pdf_image.imageHeight
        )

        if (
            original_width <= 0
            or original_height <= 0
        ):
            raise ValueError(
                f"Invalid image dimensions: "
                f"{image_path}"
            )

        width_ratio = (
            max_width
            / original_width
        )

        height_ratio = (
            max_height
            / original_height
        )

        scale = min(
            width_ratio,
            height_ratio,
        )

        pdf_image.drawWidth = (
            original_width * scale
        )

        pdf_image.drawHeight = (
            original_height * scale
        )

        pdf_image.hAlign = "CENTER"

        return pdf_image

    # ==========================================================
    # ESCAPE
    # ==========================================================

    @staticmethod
    def _escape(
        value: object,
    ) -> str:
        """
        Escape text before passing it to ReportLab Paragraph.
        """

        if value is None:
            return ""

        return html.escape(
            str(value),
            quote=False,
        )

    # ==========================================================
    # COVER
    # ==========================================================

    def _draw_cover(
        self,
        canvas,
        doc,
    ) -> None:
        """
        Draw the cover page.
        """

        width, height = A4

        canvas.saveState()

        canvas.setFillColor(
            PDFStyles.WHITE
        )

        canvas.rect(
            0,
            0,
            width,
            height,
            fill=1,
            stroke=0,
        )

        canvas.restoreState()

    # ==========================================================
    # HEADER / FOOTER
    # ==========================================================

    def _draw_page(
        self,
        canvas,
        doc,
    ) -> None:
        """
        Draw the institutional header and footer.
        """

        width, height = A4

        canvas.saveState()

        # ======================================================
        # HEADER LINE
        # ======================================================

        canvas.setStrokeColor(
            PDFStyles.PRIMARY
        )

        canvas.setLineWidth(
            0.8
        )

        canvas.line(
            PDFStyles.PAGE_MARGIN_LEFT,
            height - 1.8 * cm,
            width - PDFStyles.PAGE_MARGIN_RIGHT,
            height - 1.8 * cm,
        )

        # ======================================================
        # HEADER LEFT
        # ======================================================

        canvas.setFont(
            PDFStyles.FONT_BOLD,
            9,
        )

        canvas.setFillColor(
            PDFStyles.PRIMARY
        )

        canvas.drawString(
            PDFStyles.PAGE_MARGIN_LEFT,
            height - 1.3 * cm,
            "Ministère de l'Habitat",
        )

        # ======================================================
        # HEADER RIGHT
        # ======================================================

        canvas.setFont(
            PDFStyles.FONT,
            8,
        )

        canvas.setFillColor(
            PDFStyles.SUBTITLE
        )

        canvas.drawRightString(
            width - PDFStyles.PAGE_MARGIN_RIGHT,
            height - 1.3 * cm,
            "Immobilier IA",
        )

        # ======================================================
        # FOOTER LINE
        # ======================================================

        canvas.setStrokeColor(
            PDFStyles.BORDER
        )

        canvas.line(
            PDFStyles.PAGE_MARGIN_LEFT,
            1.5 * cm,
            width - PDFStyles.PAGE_MARGIN_RIGHT,
            1.5 * cm,
        )

        # ======================================================
        # FOOTER LEFT
        # ======================================================

        canvas.setFont(
            PDFStyles.FONT,
            8,
        )

        canvas.setFillColor(
            PDFStyles.SUBTITLE
        )

        canvas.drawString(
            PDFStyles.PAGE_MARGIN_LEFT,
            1.0 * cm,
            "Document généré automatiquement",
        )

        # ======================================================
        # FOOTER CENTER
        # ======================================================

        canvas.drawCentredString(
            width / 2,
            1.0 * cm,
            "Immobilier IA",
        )

        # ======================================================
        # FOOTER RIGHT
        # ======================================================

        canvas.drawRightString(
            width - PDFStyles.PAGE_MARGIN_RIGHT,
            1.0 * cm,
            f"Page {doc.page}",
        )

        canvas.restoreState()