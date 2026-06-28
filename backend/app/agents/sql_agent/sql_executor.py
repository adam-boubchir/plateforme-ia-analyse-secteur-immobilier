from sqlalchemy import text
from sqlalchemy.orm import Session


class SQLExecutor:
    """
    Execute validated SQL queries against the ministry database.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def execute(
        self,
        sql: str,
    ) -> list[dict]:
        """
        Execute a SQL query and return the results.
        """

        result = self.db.execute(
            text(sql)
        )

        columns = result.keys()

        rows = result.fetchall()

        return [

            dict(
                zip(
                    columns,
                    row
                )
            )

            for row in rows

        ]