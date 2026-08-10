from __future__ import annotations

from app.agents.report_agent.report_analyzer import (
    ReportAnalyzer,
)
from app.agents.report_agent.report_generator import (
    ReportGenerator,
)
from app.agents.report_agent.report_models import (
    ReportAnalysis,
    ReportRequest,
    ReportResult,
    ReportType,
)
from app.agents.report_agent.report_statistics import (
    ReportStatisticsCalculator,
)
from app.visualization.context_builder import (
    VisualizationContextBuilder,
)
from app.visualization.models import (
    ChartRecommendation,
)
from app.visualization.visualization_engine import (
    VisualizationEngine,
)

from app.agents.report_agent.report_models import DatasetMetadata

from app.pdf.pdf_generator import (
    PDFGenerator,
)

from app.pdf.pdf_report_builder import (
    PDFReportBuilder,
)

class ReportEngine:
    """
    Orchestrates the complete report generation pipeline.

    Pipeline
    --------
    ReportRequest
            ↓
    Dataset Analysis
            ↓
    Statistics Calculation
            ↓
    Visualization Context
            ↓
    Chart Recommendation
            ↓
    Markdown Generation
            ↓
    ReportResult

    Notes
    -----
    This class contains orchestration only.

    Each processing step is delegated to a dedicated component.
    """

    _DEFAULT_METHODOLOGY = (
        "This report was generated automatically from "
        "the SQL query results using the Report Agent "
        "analysis pipeline."
    )
    def __init__(
        self,
        *,
        analyzer: ReportAnalyzer,
        statistics_calculator: ReportStatisticsCalculator,
        context_builder: VisualizationContextBuilder,
        visualization_engine: VisualizationEngine,
        report_generator: ReportGenerator,
        pdf_report_builder: PDFReportBuilder,
        pdf_generator: PDFGenerator,
    ) -> None:
        self._analyzer = analyzer
        self._statistics_calculator = statistics_calculator
        self._context_builder = context_builder
        self._visualization_engine = visualization_engine
        self._report_generator = report_generator

        self._pdf_report_builder = pdf_report_builder
        self._pdf_generator = pdf_generator

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def generate(
        self,
        *,
        request: ReportRequest,
    ) -> ReportResult:
        """
        Generate a complete analytical report.

        Parameters
        ----------
        request:
            User report request.

        Returns
        -------
        ReportResult
            Generated report.
        """

        self._validate_request(
            request=request,
        )

        if not request.rows:
            return self._build_empty_report(
                request=request,
            )

        analysis = self._build_analysis(
            request=request,
        )

        charts = self._build_chart_recommendations(
            request=request,
            analysis=analysis,
        )

        markdown = self._generate_markdown(
            request=request,
            analysis=analysis,
            charts=charts,
        )

        pdf_path = self._generate_pdf(
            request=request,
            analysis=analysis,
            markdown=markdown,
        )

        return self._build_report_result(
            request=request,
            analysis=analysis,
            markdown=markdown,
            charts=charts,
            pdf_path=pdf_path,
        )

    # ==========================================================
    # ANALYSIS
    # ==========================================================

    def _build_analysis(
        self,
        *,
        request: ReportRequest,
    ) -> ReportAnalysis:
        """
        Build the structured analytical representation
        of the SQL result set.
        """

        dataset = self._analyzer.analyze(
            request.rows,
        )

        statistics = self._statistics_calculator.compute(
            rows=request.rows,
            numeric_columns=dataset.numeric_columns,
        )

        return ReportAnalysis(
            report_type=self._infer_report_type(
                dataset=dataset,
            ),
            dataset=dataset,
            statistics=statistics,
            insights=[],
        )

    # ==========================================================
    # VISUALIZATION
    # ==========================================================

    def _build_chart_recommendations(
        self,
        *,
        request: ReportRequest,
        analysis: ReportAnalysis,
    ) -> list[ChartRecommendation]:
        """
        Generate visualization recommendations for the report.
        """

        visualization_context = self._context_builder.build(
            question=request.question,
            rows=request.rows,
            dataset=analysis.dataset,
            statistics=analysis.statistics,
        )

        return self._visualization_engine.recommend(
            visualization_context,
        )

    # ==========================================================
    # REPORT GENERATION
    # ==========================================================

    def _generate_markdown(
        self,
        *,
        request: ReportRequest,
        analysis: ReportAnalysis,
        charts: list[ChartRecommendation],
    ) -> str:
        """
        Generate the Markdown report using the language model.
        """
        markdown = self._report_generator.generate(question=request.question,
                    analysis=analysis,
                    charts=charts,
                )
        return markdown.strip()

    # ==========================================================
    # RESULT
    # ==========================================================

    def _generate_pdf(
        self,
        *,
        request: ReportRequest,
        analysis: ReportAnalysis,
        markdown: str,
    ) -> str | None:
        """
        Generate the PDF report and return its path.
        """

        document = self._pdf_report_builder.create(

            title=self._build_title(
                request=request,
                analysis=analysis,
            ),

            subtitle="Rapport généré automatiquement",

            question=request.question,

            answer=markdown,

            sql=request.sql,

            rows=request.rows,

            author=request.author
            or "Ministère de l'Habitat",

        )

        pdf_path = self._pdf_generator.generate(

            document=document,

        )

        return pdf_path

    def _build_report_result(
        self,
        *,
        request: ReportRequest,
        analysis: ReportAnalysis,
        markdown: str,
        charts: list[ChartRecommendation],
        pdf_path: str | None,
    ) -> ReportResult:
        """
        Assemble the final report returned by the Report Agent.
        """

        return ReportResult(
            title=self._build_title(
                request=request,
                analysis=analysis,
            ),
            executive_summary="",
            objective=request.question,
            methodology=self._DEFAULT_METHODOLOGY,
            markdown=markdown,
            conclusions=[],
            recommendations=[],
            sections=[],
            charts=charts,
            pdf_path=pdf_path,
            generated_at=request.generated_at,
            row_count=analysis.dataset.row_count,
            column_count=analysis.dataset.column_count,
        )

    # ==========================================================
    # EMPTY REPORT
    # ==========================================================

    def _build_empty_report(
        self,
        *,
        request: ReportRequest,
    ) -> ReportResult:
        """
        Build a report result when the SQL query
        returns no rows.
        """

        return ReportResult(
            title="Rapport - Aucun résultat",
            executive_summary=(
                "Aucune donnée n'a été retournée "
                "par la requête SQL."
            ),
            objective=request.question,
            methodology=self._DEFAULT_METHODOLOGY,
            markdown=(
                "# Aucun résultat\n\n"
                "La requête exécutée n'a retourné "
                "aucune donnée exploitable pour générer "
                "une analyse."
            ),
            conclusions=[
                "Aucun résultat n'a été trouvé."
            ],
            recommendations=[
                "Vérifier les critères de recherche "
                "ou élargir la période d'analyse."
            ],
            sections=[],
            charts=[],
            pdf_path=None,
            generated_at=request.generated_at,
            row_count=0,
            column_count=0,
        )

    # ==========================================================
    # TITLE
    # ==========================================================

    @staticmethod
    def _build_title(
        *,
        request: ReportRequest,
        analysis: ReportAnalysis,
    ) -> str:
        """
        Build a report title according to the inferred report type.
        """

        report_type = analysis.report_type

        if report_type is ReportType.TREND:
            return (
                f"{analysis.report_type.value.title()} Report - "
                f"{request.question}"
            )

        if report_type is ReportType.COMPARISON:
            return "Comparative Analysis Report"

        if report_type is ReportType.STATISTICAL:
            return "Statistical Analysis Report"

        if report_type is ReportType.DISTRIBUTION:
            return "Distribution Analysis Report"

        if report_type is ReportType.DETAIL:
            return "Detailed Analysis Report"

        if report_type is ReportType.CUSTOM:
            return "Custom Analysis Report"

        return "Summary Analysis Report"

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @staticmethod
    def _validate_request(
        *,
        request: ReportRequest,
    ) -> None:
        """
        Validate the report request before processing.
        """

        if not request.question.strip():
            raise ValueError(
                "Question cannot be empty.",
            )

        if not request.sql.strip():
            raise ValueError(
                "SQL query cannot be empty.",
            )

        if not isinstance(
            request.question,
            str,
        ):
            raise TypeError(
                "Rows must be provided as a list.",
            )

        if not isinstance(
            request.sql,
            str,
        ):
            raise TypeError(
                "SQL must be provided as a list."
            )
    # ==========================================================
    # REPORT TYPE
    # ==========================================================

    @staticmethod
    def _infer_report_type(
        *,
        dataset: DatasetMetadata,
    ) -> ReportType:
        """
        Infer the most appropriate report type from the dataset.
        """

        has_datetime = bool(
            dataset.datetime_columns,
        )

        has_numeric = bool(
            dataset.numeric_columns,
        )

        has_categorical = bool(
            dataset.categorical_columns,
        )

        if has_datetime and has_numeric:
            return ReportType.TREND

        if len(dataset.numeric_columns) >= 3:
            return ReportType.STATISTICAL

        if (
            has_numeric
            and len(dataset.categorical_columns) >= 2
        ):
            return ReportType.COMPARISON

        if (
            len(dataset.categorical_columns) == 1
            and not has_numeric
        ):
            return ReportType.DISTRIBUTION

        if dataset.row_count <= 10:
            return ReportType.DETAIL

        return ReportType.SUMMARY


__all__ = (
    "ReportEngine",
)