from __future__ import annotations

from app.visualization.chart_scorer import ChartScorer
from app.visualization.chart_selector import ChartSelector
from app.visualization.intent_detector import IntentDetector
from app.visualization.models import (
    ChartRecommendation,
    VisualizationContext,
)


class VisualizationEngine:
    """
    Central orchestration engine responsible for generating
    visualization recommendations.

    Pipeline

        Context
            │
            ▼
        IntentDetector
            │
            ▼
        ChartScorer
            │
            ▼
        ChartSelector
            │
            ▼
        ChartRecommendation[]
    """

    def __init__(
        self,
        intent_detector: IntentDetector,
        chart_scorer: ChartScorer,
        chart_selector: ChartSelector,
    ) -> None:

        self._intent_detector = intent_detector
        self._chart_scorer = chart_scorer
        self._chart_selector = chart_selector

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def recommend(
        self,
        context: VisualizationContext,
    ) -> list[ChartRecommendation]:
        """
        Generate visualization recommendations.
        """

        context.intent = self._intent_detector.detect(
            context,
        )

        scores = self._chart_scorer.score(
            context,
        )

        return self._chart_selector.select(
            context=context,
            scores=scores,
        )


__all__ = [
    "VisualizationEngine",
]