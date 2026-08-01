from __future__ import annotations

import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

__all__ = [
    "SQLExecutionError",
    "SQLExecutor",
]

MAX_ROWS: int = 10_000


class SQLExecutionError(Exception):
    """
    Raised when a validated SQL query cannot be executed.
    """


class SQLExecutor:
    """
    Execute validated SQL queries.

    Responsibilities
    ----------------
    - Execute validated SQL queries.
    - Measure execution time.
    - Convert SQLAlchemy rows into dictionaries.
    - Display execution information for debugging.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def execute(
        self,
        sql: str,
    ) -> list[dict[str, Any]]:
        """
        Execute a validated SQL query and return its result.
        """

        self._display_debug_information(
            sql,
        )

        start = time.perf_counter()

        try:

            result = self.db.execute(
                text(sql),
            )

            rows = result.fetchmany(
                MAX_ROWS,
            )

            execution_time = (
                time.perf_counter() - start
            )

            self._display_execution_summary(
                execution_time=execution_time,
                row_count=len(rows),
            )

            return [
                dict(row._mapping)
                for row in rows
            ]

        except SQLAlchemyError as ex:

            raise SQLExecutionError(
                f"SQL execution failed: {ex}"
            ) from ex

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _display_debug_information(
        self,
        sql: str,
    ) -> None:
        """
        Display SQL execution information.
        """

        try:
            # SQL Server specific
            db_name = self.db.execute(
                text("SELECT DB_NAME()"),
            ).scalar()

        except Exception:
            db_name = "Unknown"

        print()
        print("=" * 100)
        print("SQL EXECUTOR")
        print("=" * 100)
        print(f"Database : {db_name}")
        print()
        print("SQL")
        print("-" * 100)
        print(sql)
        print("=" * 100)
        print()

    def _display_execution_summary(
        self,
        execution_time: float,
        row_count: int,
    ) -> None:
        """
        Display SQL execution statistics.
        """

        print()
        print("=" * 100)
        print("SQL EXECUTION")
        print("=" * 100)
        print(
            f"Execution Time : {execution_time:.3f} sec"
        )
        print(
            f"Returned Rows  : {row_count}"
        )
        print("=" * 100)
        print()