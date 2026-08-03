from __future__ import annotations

from datetime import (
    date,
    datetime,
)
from numbers import Real
from typing import Any

from app.agents.report_agent.report_models import (
    DatasetMetadata,
)


class ReportAnalyzer:
    """
    Analyse a SQL result set and extract structural metadata.

    This component is responsible only for describing the dataset.
    It does not compute statistics.
    """

    _GEOGRAPHIC_KEYWORDS = frozenset({
        "region",
        "région",
        "province",
        "ville",
        "commune",
        "territoire",
        "city",
        "prefecture",
        "localisation",
        "location",
    })

    def analyze(
        self,
        rows: list[dict[str, Any]],
    ) -> DatasetMetadata:
        """
        Analyse the dataset structure.
        """

        if not rows:
            return DatasetMetadata(
                row_count=0,
                column_count=0,
                columns=[],
                numeric_columns=[],
                categorical_columns=[],
                datetime_columns=[],
                geographic_columns=[],
            )

        columns = list(rows[0].keys())

        numeric_columns: list[str] = []
        categorical_columns: list[str] = []
        datetime_columns: list[str] = []
        geographic_columns: list[str] = []

        for column in columns:

            values = [
                row[column]
                for row in rows
                if row.get(column) is not None
            ]

            if not values:
                continue

            if all(
                isinstance(value, Real)
                for value in values
            ):
                numeric_columns.append(column)

            elif all(
                self._is_datetime(value)
                for value in values
            ):
                datetime_columns.append(column)

            else:
                categorical_columns.append(column)

            if self._is_geographic(column):
                geographic_columns.append(column)

        return DatasetMetadata(
            row_count=len(rows),
            column_count=len(columns),
            columns=columns,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            datetime_columns=datetime_columns,
            geographic_columns=geographic_columns,
        )

    @staticmethod
    def _is_datetime(
        value: Any,
    ) -> bool:
        """
        Return True if the value is a date or datetime.
        """

        return isinstance(
            value,
            (
                date,
                datetime,
            ),
        )

    @classmethod
    def _is_geographic(
        cls,
        column: str,
    ) -> bool:
        """
        Detect geographic columns from their names.
        """

        normalized = column.lower()

        return any(
            keyword in normalized
            for keyword in cls._GEOGRAPHIC_KEYWORDS
        )


__all__ = [
    "ReportAnalyzer",
]