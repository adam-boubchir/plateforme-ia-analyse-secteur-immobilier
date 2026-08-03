from __future__ import annotations

import logging
import time
from typing import Any

from sqlalchemy import Row, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

__all__ = (
    "SQLExecutionError",
    "SQLExecutor",
)

# ==========================================================
# CONSTANTS
# ==========================================================

logger = logging.getLogger(__name__)

_MAX_RESULT_ROWS = 10_000


class SQLExecutionError(Exception):
    """
    Raised when a validated SQL query cannot be executed.
    """


class SQLExecutor:
    """
    Execute validated SQL queries.

    Responsibilities
    ----------------
    - Execute validated SQL statements.
    - Convert SQLAlchemy rows into dictionaries.
    - Log execution information.
    - Raise execution-specific exceptions.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        self._db = db

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def execute(
        self,
        *,
        sql: str,
    ) -> list[dict[str, Any]]:
        """
        Execute a validated SQL query.

        Args:
            sql:
                Validated SQL query.

        Returns:
            Query result as a list of dictionaries.

        Raises:
            SQLExecutionError:
                If the query cannot be executed.
        """

        self._log_debug_information(
            sql=sql,
        )

        start_time = time.perf_counter()

        try:

            result = self._db.execute(
                text(sql),
            )

            rows = result.fetchmany(
                _MAX_RESULT_ROWS,
            )

        except SQLAlchemyError as exception:

            raise SQLExecutionError(
                f"SQL execution failed: {exception}"
            ) from exception

        execution_time = (
            time.perf_counter() - start_time
        )

        self._log_execution_summary(
            execution_time=execution_time,
            row_count=len(rows),
        )

        converted_rows = self._convert_rows(
            rows=rows,
        )

        return converted_rows

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _convert_rows(
        *,
        rows: list[Row[Any]],
    ) -> list[dict[str, Any]]:
        """
        Convert SQLAlchemy rows into dictionaries.
        """

        converted_rows = [
            dict(
                row._mapping,
            )
            for row in rows
        ]

        return converted_rows

    def _get_database_name(
        self,
    ) -> str:
        """
        Return the current database name.
        """

        try:

            database_name = self._db.execute(
                text(
                    "SELECT DB_NAME()",
                )
            ).scalar()

            database_name = str(
                database_name,
            )

        except SQLAlchemyError:

            database_name = "Unknown"

        return database_name

    def _log_debug_information(
        self,
        *,
        sql: str,
    ) -> None:
        """
        Log debug information before executing the query.
        """

        database_name = self._get_database_name()

        logger.debug(
            "Database=%s SQL=%s",
            database_name,
            sql,
        )

    @staticmethod
    def _log_execution_summary(
        *,
        execution_time: float,
        row_count: int,
    ) -> None:
        """
        Log execution statistics.
        """

        logger.info(
            "SQL executed in %.3fs (%d rows)",
            execution_time,
            row_count,
        )