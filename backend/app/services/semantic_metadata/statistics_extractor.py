from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

__all__ = ["StatisticsExtractor"]


class StatisticsExtractor:
    """
    Extract statistics from a database column.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def extract(
        self,
        table_name: str,
        column_name: str,
        data_type: str,
    ) -> dict[str, Any]:
        """
        Extract basic statistics for one database column.
        """

        result: dict[str, Any] = {
            "min_value": None,
            "max_value": None,
            "distinct_count": 0,
        }

        if not self._is_valid_identifier(table_name):
            return result

        if not self._is_valid_identifier(column_name):
            return result

        query = text(
            f"""
            SELECT
                COUNT(DISTINCT [{column_name}]) AS distinct_count,
                MIN([{column_name}]) AS min_value,
                MAX([{column_name}]) AS max_value
            FROM [{table_name}]
            """
        )

        try:
            row = self.db.execute(query).first()

            if row is None:
                return result

            result["distinct_count"] = row.distinct_count
            result["min_value"] = row.min_value
            result["max_value"] = row.max_value

        except Exception:
            return result

        return result

    @staticmethod
    def _is_valid_identifier(
        identifier: str,
    ) -> bool:
        """
        Validate a SQL identifier.
        """

        return identifier.replace("_", "").isalnum()