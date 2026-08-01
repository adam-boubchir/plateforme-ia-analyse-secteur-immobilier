from __future__ import annotations

from typing import Final

from sqlalchemy import text
from sqlalchemy.orm import Session

__all__ = ["ExampleValueExtractor"]

MAX_EXAMPLES: Final[int] = 20

TEXT_TYPES: Final[frozenset[str]] = frozenset(
    {
        "char",
        "varchar",
        "nvarchar",
        "text",
        "ntext",
    }
)


class ExampleValueExtractor:
    """
    Extract representative values from a text column.
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
    ) -> str:
        """
        Extract representative values from one column.
        """

        if not self._is_text_column(data_type):
            return ""

        if not self._is_valid_identifier(table_name):
            return ""

        if not self._is_valid_identifier(column_name):
            return ""

        query = text(
            f"""
            SELECT DISTINCT TOP ({MAX_EXAMPLES})
                [{column_name}]
            FROM [{table_name}]
            WHERE [{column_name}] IS NOT NULL
            ORDER BY [{column_name}]
            """
        )

        try:
            result = self.db.execute(query)

            values = [
                value
                for row in result
                if (value := str(row[0]).strip())
            ]

            return " | ".join(values)

        except Exception:
            return ""

    @staticmethod
    def _is_text_column(
        data_type: str,
    ) -> bool:
        """
        Return whether the SQL type is textual.
        """

        normalized = data_type.casefold()

        return any(
            sql_type in normalized
            for sql_type in TEXT_TYPES
        )

    @staticmethod
    def _is_valid_identifier(
        identifier: str,
    ) -> bool:
        """
        Validate a SQL identifier.
        """

        return identifier.replace("_", "").isalnum()