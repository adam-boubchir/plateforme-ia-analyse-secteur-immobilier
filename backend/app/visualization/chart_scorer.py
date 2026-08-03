from __future__ import annotations

from app.visualization.models import (
    ChartScore,
    ChartType,
    VisualizationContext,
    VisualizationIntent,
)


class ChartScorer:
    """
    Compute a score for every supported chart.

    This component only assigns scores.
    It never decides which chart is finally selected.
    """

    _INTENT_RULES: dict[
        VisualizationIntent,
        tuple[tuple[ChartType, float, str], ...],
    ] = {
        VisualizationIntent.COMPARISON: (
            (ChartType.BAR, 40, "Comparison intent"),
            (ChartType.HORIZONTAL_BAR, 35, "Comparison intent"),
        ),
        VisualizationIntent.TREND: (
            (ChartType.LINE, 45, "Trend intent"),
            (ChartType.AREA, 35, "Trend intent"),
        ),
        VisualizationIntent.DISTRIBUTION: (
            (ChartType.HISTOGRAM, 40, "Distribution intent"),
        ),
        VisualizationIntent.RANKING: (
            (ChartType.HORIZONTAL_BAR, 45, "Ranking intent"),
        ),
        VisualizationIntent.GEOGRAPHIC: (
            (ChartType.MAP, 60, "Geographic intent"),
        ),
        VisualizationIntent.CORRELATION: (
            (ChartType.SCATTER, 50, "Correlation intent"),
        ),
        VisualizationIntent.COMPOSITION: (
            (ChartType.PIE, 40, "Composition intent"),
            (ChartType.DONUT, 35, "Composition intent"),
        ),
        VisualizationIntent.SUMMARY: (
            (ChartType.TABLE, 20, "Summary intent"),
            (ChartType.KPI_CARD, 25, "Summary intent"),
        ),
    }

    def score(
        self,
        context: VisualizationContext,
    ) -> list[ChartScore]:

        scores = {
            chart: ChartScore(chart_type=chart)
            for chart in ChartType
        }

        self._score_by_intent(context, scores)
        self._score_by_dataset(context, scores)
        self._score_by_statistics(context, scores)

        return sorted(
            scores.values(),
            key=lambda item: item.score,
            reverse=True,
        )

    def _score_by_intent(
        self,
        context: VisualizationContext,
        scores: dict[ChartType, ChartScore],
    ) -> None:

        for chart, value, reason in self._INTENT_RULES.get(
            context.intent,
            (),
        ):
            self._add(
                scores=scores,
                chart=chart,
                value=value,
                reason=reason,
            )

    def _score_by_dataset(
        self,
        context: VisualizationContext,
        scores: dict[ChartType, ChartScore],
    ) -> None:

        dataset = context.dataset

        if dataset.datetime_columns:
            self._add(
                scores=scores,
                chart=ChartType.LINE,
                value=20,
                reason="Datetime column detected",
            )

            self._add(
                scores=scores,
                chart=ChartType.AREA,
                value=15,
                reason="Datetime column detected",
            )

        if dataset.categorical_columns and dataset.numeric_columns:
            self._add(
                scores=scores,
                chart=ChartType.BAR,
                value=20,
                reason="Categorical + numeric dataset",
            )

            self._add(
                scores=scores,
                chart=ChartType.HORIZONTAL_BAR,
                value=15,
                reason="Categorical + numeric dataset",
            )

        if len(dataset.numeric_columns) >= 2:
            self._add(
                scores=scores,
                chart=ChartType.SCATTER,
                value=20,
                reason="Multiple numeric columns",
            )

        if dataset.geographic_columns:
            self._add(
                scores=scores,
                chart=ChartType.MAP,
                value=30,
                reason="Geographic columns detected",
            )

    def _score_by_statistics(
        self,
        context: VisualizationContext,
        scores: dict[ChartType, ChartScore],
    ) -> None:

        if not context.statistics.statistics:
            return

        self._add(
            scores=scores,
            chart=ChartType.TABLE,
            value=10,
            reason="Statistics available",
        )

        self._add(
            scores=scores,
            chart=ChartType.KPI_CARD,
            value=15,
            reason="Statistics available",
        )

    @staticmethod
    def _add(
        *,
        scores: dict[ChartType, ChartScore],
        chart: ChartType,
        value: float,
        reason: str,
    ) -> None:

        candidate = scores[chart]

        candidate.score += value
        candidate.reasons.append(reason)


__all__ = [
    "ChartScorer",
]