from __future__ import annotations

from app.visualization.models import (
    ChartRecommendation,
    ChartScore,
    ChartType,
    VisualizationContext,
)


class ChartSelector:
    """
    Select the best visualization candidates.

    Responsibilities:
    - filter candidates
    - limit recommendations
    - enrich recommendations with default metadata
    """

    DEFAULT_THRESHOLD = 20.0
    DEFAULT_LIMIT = 3

    def select(
        self,
        *,
        context: VisualizationContext,
        scores: list[ChartScore],
        limit: int = DEFAULT_LIMIT,
        threshold: float = DEFAULT_THRESHOLD,
    ) -> list[ChartRecommendation]:
        print(__file__)
        filtered_scores = [
            score
            for score in scores
            if score.score >= threshold
        ][:limit]

        return [
            ChartRecommendation(
                chart_type=score.chart_type,
                title=self._build_title(
                    context=context,
                    chart=score,
                ),
                x_axis=self._default_x_axis(
                    context=context,
                    chart=score,
                ),
                y_axis=self._default_y_axis(
                    context=context,
                    chart=score,
                ),
                score=score.score,
                reasons=tuple(score.reasons),
            )
            for score in filtered_scores
        ]

    @staticmethod
    def _default_x_axis(
        *,
        context: VisualizationContext,
        chart: ChartScore,
    ) -> str | None:

        dataset = context.dataset

        if chart.chart_type in (
            ChartType.LINE,
            ChartType.AREA,
        ):
            if dataset.datetime_columns:
                return dataset.datetime_columns[0]

        if dataset.categorical_columns:
            return dataset.categorical_columns[0]

        return None

    @staticmethod
    def _default_y_axis(
        *,
        context: VisualizationContext,
        chart: ChartScore,
    ) -> str | None:

        dataset = context.dataset

        if dataset.numeric_columns:
            return dataset.numeric_columns[0]

        return None

    @staticmethod
    def _build_title(
        *,
        context: VisualizationContext,
        chart: ChartScore,
    ) -> str:

        return (
            f"{chart.chart_type.value.replace('_', ' ').title()} "
            f"for '{context.question}'"
        )


__all__ = [
    "ChartSelector",
]