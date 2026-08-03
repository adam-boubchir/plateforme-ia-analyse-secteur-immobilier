from __future__ import annotations

from numbers import Real
from statistics import (
    mean,
    median,
    stdev,
)
from typing import Any

from app.agents.report_agent.report_models import (
    NumericStatistic,
    ReportStatistics,
)


class ReportStatisticsCalculator:
    """
    Compute descriptive statistics for numeric columns
    extracted from a SQL result set.
    """

    def compute(
        self,
        rows: list[dict[str, Any]],
        numeric_columns: list[str],
    ) -> ReportStatistics:
        """
        Compute descriptive statistics for each numeric column.
        """

        statistics = [
            self._build_statistic(
                column=column,
                values=values,
            )
            for column in numeric_columns
            if (
                values := self._extract_numeric_values(
                    rows=rows,
                    column=column,
                )
            )
        ]

        return ReportStatistics(
            statistics=statistics,
        )

    @staticmethod
    def _build_statistic(
        *,
        column: str,
        values: list[float],
    ) -> NumericStatistic:
        """
        Build statistics for a single numeric column.
        """

        values = sorted(values)

        count = len(values)

        if count == 0:
            raise ValueError(
                f"No numeric values found for column '{column}'."
            )

        def percentile(data: list[float], p: float) -> float:
            """
            Compute a percentile using linear interpolation.
            """

            if len(data) == 1:
                return data[0]

            k = (len(data) - 1) * p
            f = int(k)
            c = min(f + 1, len(data) - 1)

            if f == c:
                return data[f]

            return data[f] + (data[c] - data[f]) * (k - f)

        return NumericStatistic(
            column=column,
            minimum=min(values),
            maximum=max(values),
            average=mean(values),
            median=median(values),
            std=stdev(values) if count > 1 else 0.0,
            total=sum(values),

            count=count,
            variance=(stdev(values) ** 2) if count > 1 else 0.0,
            q1=percentile(values, 0.25),
            q3=percentile(values, 0.75),
            missing_values=0,
        )
    @staticmethod
    def _extract_numeric_values(
        *,
        rows: list[dict[str, Any]],
        column: str,
    ) -> list[float]:
        """
        Extract numeric values from one column.
        """

        values: list[float] = []

        for row in rows:

            value = row.get(column)

            if isinstance(value, Real):
                values.append(float(value))

        return values


__all__ = [
    "ReportStatisticsCalculator",
]