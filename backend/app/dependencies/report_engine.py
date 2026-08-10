from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.report_agent.report_analyzer import (
    ReportAnalyzer,
)
from app.agents.report_agent.report_engine import (
    ReportEngine,
)
from app.agents.report_agent.report_generator import (
    ReportGenerator,
)
from app.agents.report_agent.report_prompt_builder import (
    ReportPromptBuilder,
)
from app.agents.report_agent.report_statistics import (
    ReportStatisticsCalculator,
)
from app.dependencies.llm import (
    get_llm_service,
)
from app.visualization.chart_scorer import (
    ChartScorer,
)
from app.visualization.chart_selector import (
    ChartSelector,
)
from app.visualization.context_builder import (
    VisualizationContextBuilder,
)
from app.visualization.intent_detector import (
    IntentDetector,
)
from app.visualization.visualization_engine import (
    VisualizationEngine,
)
from app.pdf.pdf_generator import (
    PDFGenerator,
)

from app.pdf.pdf_report_builder import (
    PDFReportBuilder,
)

from app.storage.storage_service import (
    StorageService,
)

__all__ = (
    "get_report_engine",
)


def get_report_engine(
    *,
    db: Session,
) -> ReportEngine:
    """
    Build and configure the ReportEngine.

    Pipeline
    --------
    ReportAnalyzer
            ↓
    ReportStatisticsCalculator
            ↓
    VisualizationContextBuilder
            ↓
    VisualizationEngine
            ↓
    ReportGenerator
            ↓
    ReportEngine

    Parameters
    ----------
    db:
        Application database session.

    Returns
    -------
    ReportEngine
        Fully configured ReportEngine instance.
    """

    analyzer = ReportAnalyzer()

    statistics_calculator = ReportStatisticsCalculator()

    context_builder = VisualizationContextBuilder()

    visualization_engine = VisualizationEngine(
        intent_detector=IntentDetector(),
        chart_scorer=ChartScorer(),
        chart_selector=ChartSelector(),
    )

    llm_service = get_llm_service(
        db=db,
    )

    prompt_builder = ReportPromptBuilder()

    report_generator = ReportGenerator(
        llm_service=llm_service,
        prompt_builder=prompt_builder,
    )

    storage_service = StorageService()

    pdf_report_builder = PDFReportBuilder()

    pdf_generator = PDFGenerator(
        storage_service=storage_service,
    )

    return ReportEngine(
        analyzer=analyzer,
        statistics_calculator=statistics_calculator,
        context_builder=context_builder,
        visualization_engine=visualization_engine,
        report_generator=report_generator,
        pdf_report_builder=pdf_report_builder,
        pdf_generator=pdf_generator,
    )