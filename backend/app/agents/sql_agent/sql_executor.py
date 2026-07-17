import time

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class SQLExecutionError(Exception):
    """
    Raised when a SQL query cannot be executed.
    """
    pass


class SQLExecutor:
    """
    Execute validated SQL queries.

    Responsibilities
    ----------------
    • Execute SQL safely
    • Log execution
    • Measure execution time
    • Convert SQLAlchemy rows into dictionaries
    """

    MAX_ROWS = 10000

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def execute(
        self,
        sql: str,
    ) -> list[dict]:
        """
        Execute a SQL query and return the result.
        """

        self._print_debug(sql)

        start = time.perf_counter()

        try:

            result = self.db.execute(
                text(sql)
            )

            columns = result.keys()

            rows = result.fetchmany(
                self.MAX_ROWS
            )

            execution_time = (
                time.perf_counter() - start
            )

            print()

            print("=" * 100)

            print("SQL EXECUTION")

            print("=" * 100)

            print(
                f"Execution Time : {execution_time:.3f} sec"
            )

            print(
                f"Returned Rows  : {len(rows)}"
            )

            print("=" * 100)

            print()

            return [

                dict(zip(columns, row))

                for row in rows

            ]

        except SQLAlchemyError as ex:

            raise SQLExecutionError(
                str(ex)
            ) from ex

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _print_debug(
        self,
        sql: str,
    ) -> None:
        """
        Display useful debugging information.
        """

        try:

            db_name = self.db.execute(
                text(
                    "SELECT DB_NAME()"
                )
            ).scalar()

        except Exception:

            db_name = "Unknown"

        print()

        print("=" * 100)

        print("SQL EXECUTOR")

        print("=" * 100)

        print(
            f"Database : {db_name}"
        )

        print()

        print("SQL")

        print("-" * 100)

        print(sql)

        print("=" * 100)

        print()