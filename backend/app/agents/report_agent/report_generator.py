from __future__ import annotations

from typing import Any

from app.agents.report_agent.report_models import ReportAnalysis
from app.agents.report_agent.report_prompt_builder import ReportPromptBuilder
from app.services.llm_service import LLMService
from app.visualization.models import ChartRecommendation


class ReportGenerator:
    """
    Generate analytical reports using the configured language model.

    Responsibilities
    ----------------
    - Build the prompt.
    - Invoke the LLM.
    - Return the generated Markdown report.

    No business logic is implemented here.
    """

    def __init__(
        self,
        *,
        llm_service: LLMService,
        prompt_builder: ReportPromptBuilder,
    ) -> None:
        self._llm_service = llm_service
        self._prompt_builder = prompt_builder

    def _build_prompt(
        self,
        *,
        question: str,
        analysis: ReportAnalysis,
        charts: list[ChartRecommendation],
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Build the prompt sent to the LLM.
        """

        return self._prompt_builder.build(
            question=question,
            analysis=analysis,
            charts=charts,
            rows=rows,
        )

    def generate(
        self,
        *,
        question: str,
        analysis: ReportAnalysis,
        charts: list[ChartRecommendation],
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Generate a Markdown report.

        Parameters
        ----------
        question:
            Original user question.

        analysis:
            Structured analytical information.

        charts:
            Recommended visualizations.

        rows:
            Raw rows returned by the SQL query.

        Returns
        -------
        str
            Generated report in Markdown format.

        Raises
        ------
        RuntimeError
            If the LLM returns an empty response.
        """

        prompt = self._build_prompt(
            question=question,
            analysis=analysis,
            charts=charts,
            rows=rows,
        )

        report = self._llm_service.generate(
            agent_name="report_agent",
            prompt=prompt,
        )

        report = report.strip()

        if not report:
            raise RuntimeError(
                "The language model returned an empty report.",
            )

        return report


__all__ = (
    "ReportGenerator",
)