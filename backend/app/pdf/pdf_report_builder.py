from __future__ import annotations

from pathlib import Path
from statistics import mean, median
from typing import Any

from app.pdf.pdf_models import (
    PDFDocument,
    PDFKPI,
    PDFMetadata,
    PDFSection,
    PDFTable,
)

from app.pdf.chart_generator import ChartGenerator


__all__ = (
    "PDFReportBuilder",
)


class PDFReportBuilder:
    """
    Builds the structured analytical PDF document.

    Responsibilities
    ----------------
    - Build the report structure.
    - Select relevant KPIs.
    - Create a limited data preview.
    - Request chart generation.
    - Add methodology and conclusion sections.

    The builder does not generate the PDF itself.
    It prepares a PDFDocument consumed by PDFGenerator.
    """

    # ==========================================================
    # CONFIGURATION
    # ==========================================================

    PREVIEW_ROWS = 15

    # Maximum number of KPI cards.
    MAX_KPIS = 5

    # Column names that should normally not be used
    # as analytical measures.
    IGNORED_NUMERIC_COLUMN_KEYWORDS = (
        "id",
        "code",
        "annee",
        "année",
        "year",
        "mois",
        "month",
        "jour",
        "day",
        "latitude",
        "longitude",
        "lat",
        "lon",
    )

    def __init__(self) -> None:

        self._document: PDFDocument | None = None

        self._chart_generator = ChartGenerator(
            output_directory=Path(
                "storage/charts",
            ),
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def create(
        self,
        *,
        title: str,
        subtitle: str,
        question: str,
        answer: str,
        sql: str | None = None,
        rows: list[dict] | None = None,
        author: str = "Ministère de l'Habitat",
    ) -> PDFDocument:
        """
        Build the complete PDFDocument.
        """

        rows = rows or []

        self._document = PDFDocument(
            title=title,
            subtitle=subtitle,
            author=author,
            content=question,
            metadata=self._build_metadata(
                title=title,
            ),
        )

        # ------------------------------------------------------
        # 1. EXECUTIVE ANALYSIS
        # ------------------------------------------------------

        self._add_analysis_section(
            answer=answer,
        )

        # ------------------------------------------------------
        # 2. KEY METRICS
        # ------------------------------------------------------

        self._add_statistics_section(
            rows=rows,
        )

        # ------------------------------------------------------
        # 3. CHARTS
        # ------------------------------------------------------

        self._add_charts(
            rows=rows,
        )

        # ------------------------------------------------------
        # 4. DATA PREVIEW
        # ------------------------------------------------------

        self._add_results_table(
            rows=rows,
        )

        # ------------------------------------------------------
        # 5. SQL
        # ------------------------------------------------------

        self._add_sql_section(
            sql=sql,
        )

        # ------------------------------------------------------
        # 6. METHODOLOGY
        # ------------------------------------------------------

        self._add_methodology()

        # ------------------------------------------------------
        # 7. CONCLUSION
        # ------------------------------------------------------

        self._add_conclusion()

        return self._document

    # ==========================================================
    # METADATA
    # ==========================================================

    def _build_metadata(
        self,
        *,
        title: str,
    ) -> PDFMetadata:
        """
        Build PDF metadata.
        """

        return PDFMetadata(
            title=title,
            author="Ministère de l'Habitat",
            subject="Rapport d'analyse du secteur immobilier",
            keywords=[
                "Immobilier",
                "Habitat",
                "Analyse",
                "Intelligence artificielle",
                "SQL",
            ],
        )

    # ==========================================================
    # ANALYSIS
    # ==========================================================

    def _add_analysis_section(
        self,
        *,
        answer: str,
    ) -> None:
        """
        Add the AI-generated analytical summary.
        """

        if not answer:
            return

        self._document.sections.append(
            PDFSection(
                title="Résumé et analyse",
                content=answer.strip(),
            )
        )

    # ==========================================================
    # STATISTICS / KPI
    # ==========================================================

    def _add_statistics_section(
        self,
        *,
        rows: list[dict],
    ) -> None:
        """
        Build relevant KPI cards from the returned data.

        Important:
        Numeric dimensions such as years, IDs and codes
        are excluded from statistical calculations.
        """

        if not rows:
            return

        # ------------------------------------------------------
        # RESULT COUNT
        # ------------------------------------------------------

        self._document.kpis.append(
            PDFKPI(
                label="Résultats",
                value=str(len(rows)),
                unit="lignes",
                description=(
                    "Nombre de lignes retournées "
                    "par la requête"
                ),
            )
        )

        # ------------------------------------------------------
        # ANALYTICAL MEASURE
        # ------------------------------------------------------

        measure = self._detect_measure_column(
            rows=rows,
        )

        if measure is None:
            return

        column_name, values = measure

        if not values:
            return

        # ------------------------------------------------------
        # MINIMUM
        # ------------------------------------------------------

        self._document.kpis.append(
            PDFKPI(
                label="Minimum",
                value=self._format_number(
                    min(values),
                ),
                description=(
                    f"Valeur minimale de "
                    f"{column_name}"
                ),
            )
        )

        # ------------------------------------------------------
        # MAXIMUM
        # ------------------------------------------------------

        self._document.kpis.append(
            PDFKPI(
                label="Maximum",
                value=self._format_number(
                    max(values),
                ),
                description=(
                    f"Valeur maximale de "
                    f"{column_name}"
                ),
            )
        )

        # ------------------------------------------------------
        # AVERAGE
        # ------------------------------------------------------

        self._document.kpis.append(
            PDFKPI(
                label="Moyenne",
                value=self._format_number(
                    mean(values),
                ),
                description=(
                    f"Moyenne de "
                    f"{column_name}"
                ),
            )
        )

        # ------------------------------------------------------
        # MEDIAN
        # ------------------------------------------------------

        self._document.kpis.append(
            PDFKPI(
                label="Médiane",
                value=self._format_number(
                    median(values),
                ),
                description=(
                    f"Médiane de "
                    f"{column_name}"
                ),
            )
        )

    # ==========================================================
    # MEASURE DETECTION
    # ==========================================================

    def _detect_measure_column(
        self,
        *,
        rows: list[dict],
    ) -> tuple[str, list[float]] | None:
        """
        Detect the most relevant numerical measure.

        Returns:
            (column_name, numeric_values)
        """

        if not rows:
            return None

        columns = list(
            rows[0].keys()
        )

        candidates: list[
            tuple[str, list[float], int]
        ] = []

        for column in columns:

            column_lower = (
                str(column)
                .strip()
                .lower()
            )

            # --------------------------------------------------
            # IGNORE DIMENSION-LIKE NUMERIC COLUMNS
            # --------------------------------------------------

            if any(
                keyword in column_lower
                for keyword
                in self.IGNORED_NUMERIC_COLUMN_KEYWORDS
            ):
                continue

            values: list[float] = []

            for row in rows:

                value = row.get(
                    column,
                )

                if value is None:
                    continue

                if isinstance(
                    value,
                    bool,
                ):
                    continue

                if isinstance(
                    value,
                    (int, float),
                ):
                    values.append(
                        float(value),
                    )

            if not values:
                continue

            # --------------------------------------------------
            # SCORE COLUMN
            # --------------------------------------------------

            score = self._score_measure_column(
                column_name=column_lower,
            )

            candidates.append(
                (
                    str(column),
                    values,
                    score,
                )
            )

        if not candidates:
            return None

        # Highest semantic score first,
        # then number of usable values.
        candidates.sort(
            key=lambda item: (
                item[2],
                len(item[1]),
            ),
            reverse=True,
        )

        column_name, values, _ = (
            candidates[0]
        )

        return (
            column_name,
            values,
        )

    # ==========================================================
    # MEASURE SCORING
    # ==========================================================

    def _score_measure_column(
        self,
        *,
        column_name: str,
    ) -> int:
        """
        Give preference to columns that usually
        represent analytical measurements.
        """

        score = 0

        positive_keywords = (
            "prix",
            "price",
            "montant",
            "amount",
            "cout",
            "coût",
            "cost",
            "valeur",
            "value",
            "loyer",
            "rent",
            "salaire",
            "revenu",
            "revenue",
            "taux",
            "rate",
            "pourcentage",
            "percentage",
            "quantite",
            "quantité",
            "quantity",
            "volume",
            "consommation",
            "consumption",
            "surface",
            "superficie",
            "population",
            "nombre",
            "total",
            "moyenne",
            "average",
        )

        for keyword in positive_keywords:

            if keyword in column_name:
                score += 10

        return score

    # ==========================================================
    # SQL
    # ==========================================================

    def _add_sql_section(
        self,
        *,
        sql: str | None,
    ) -> None:
        """
        Add the SQL query used to retrieve the data.
        """

        if not sql:
            return

        self._document.sections.append(
            PDFSection(
                title="Requête SQL exécutée",
                content=sql.strip(),
            )
        )

    # ==========================================================
    # RESULTS TABLE
    # ==========================================================

    def _add_results_table(
        self,
        *,
        rows: list[dict],
    ) -> None:
        """
        Add a limited preview of the SQL results.
        """

        if not rows:
            return

        headers = list(
            rows[0].keys()
        )

        preview = rows[
            : self.PREVIEW_ROWS
        ]

        values: list[list[str]] = []

        for row in preview:

            current_row: list[str] = []

            for column in headers:

                value = row.get(
                    column,
                    "",
                )

                current_row.append(
                    self._format_value(
                        value,
                    )
                )

            values.append(
                current_row,
            )

        self._document.tables.append(
            PDFTable(
                title=(
                    "Aperçu des résultats "
                    f"({len(preview)} lignes sur "
                    f"{len(rows)})"
                ),
                headers=[
                    str(header)
                    for header in headers
                ],
                rows=values,
            )
        )

    # ==========================================================
    # CHARTS
    # ==========================================================

    def _add_charts(
        self,
        *,
        rows: list[dict],
    ) -> None:
        """
        Generate visualizations from the returned data.
        """

        if not rows:
            return

        images = self._chart_generator.generate(
            rows=rows,
        )

        if not images:
            return

        self._document.images.extend(
            images,
        )

    # ==========================================================
    # METHODOLOGY
    # ==========================================================

    def _add_methodology(
        self,
    ) -> None:
        """
        Add a concise explanation of the analytical pipeline.
        """

        self._document.sections.append(
            PDFSection(
                title="Méthodologie",
                content=(
                    "Ce rapport est généré automatiquement "
                    "à partir des données disponibles dans "
                    "la base de données du Ministère. "
                    "La question formulée en langage naturel "
                    "est interprétée par l'agent d'intelligence "
                    "artificielle, puis transformée en requête "
                    "SQL. Les résultats retournés sont ensuite "
                    "analysés afin de produire une synthèse, "
                    "des indicateurs clés et des visualisations."
                ),
            )
        )

    # ==========================================================
    # CONCLUSION
    # ==========================================================

    def _add_conclusion(
        self,
    ) -> None:
        """
        Add a neutral conclusion section.
        """

        self._document.sections.append(
            PDFSection(
                title="Conclusion",
                content=(
                    "Les résultats présentés dans ce rapport "
                    "permettent de synthétiser les données "
                    "retournées par la requête et d'en faciliter "
                    "l'interprétation à travers des indicateurs "
                    "et des visualisations adaptés."
                ),
            )
        )

    # ==========================================================
    # DATA HELPERS
    # ==========================================================

    def _format_value(
        self,
        value: Any,
    ) -> str:
        """
        Format a value for display inside the PDF table.
        """

        if value is None:
            return "—"

        if isinstance(
            value,
            bool,
        ):
            return "Oui" if value else "Non"

        if isinstance(
            value,
            float,
        ):
            return self._format_number(
                value,
            )

        return str(value)

    def _format_number(
        self,
        value: float,
    ) -> str:
        """
        Format numbers using French-style separators.
        """

        return (
            f"{value:,.2f}"
            .replace(",", " ")
            .replace(".", ",")
        )