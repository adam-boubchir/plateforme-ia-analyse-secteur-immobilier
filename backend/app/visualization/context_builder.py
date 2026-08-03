from __future__ import annotations

from app.agents.report_agent.report_models import (
    DatasetMetadata,
    ReportStatistics,
)
from app.visualization.models import (
    DatasetInfo,
    StatisticsInfo,
    VisualizationContext,
)


class VisualizationContextBuilder:
    """
    Build a VisualizationContext from Report Agent outputs.

    This class acts as an anti-corruption layer between the Report Agent
    and the Visualization module.
    """

    def build(
        self,
        *,
        question: str,
        rows: list[dict],
        dataset: DatasetMetadata,
        statistics: ReportStatistics,
    ) -> VisualizationContext:
        """
        Convert Report Agent models into Visualization models.
        """

        dataset_info = DatasetInfo(
            categorical_columns=list(dataset.categorical_columns),
            numeric_columns=list(dataset.numeric_columns),
            datetime_columns=list(dataset.datetime_columns),
            geographic_columns=self._detect_geographic_columns(
                dataset.columns,
            ),
        )

        statistics_info = StatisticsInfo(
            statistics={
                stat.column: stat
                for stat in statistics.statistics
            }
        )

        return VisualizationContext(
            question=question,
            rows=rows,
            dataset=dataset_info,
            statistics=statistics_info,
        )

    @staticmethod
    def _detect_geographic_columns(
        columns: list[str],
    ) -> list[str]:
        """
        Detect geographic columns using common naming conventions.
        """

        keywords = {
            "region",
            "région",
            "province",
            "ville",
            "commune",
            "territoire",
            "localisation",
            "locality",
            "city",
            "prefecture",
        }

        detected: list[str] = []

        for column in columns:

            normalized = column.lower()

            if any(
                keyword in normalized
                for keyword in keywords
            ):
                detected.append(column)

        return detected


__all__ = [
    "VisualizationContextBuilder",
]