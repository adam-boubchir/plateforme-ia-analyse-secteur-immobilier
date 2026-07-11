from sqlalchemy import text
from sqlalchemy.orm import Session


class SQLExecutor:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def execute(
        self,
        sql: str,
    ) -> list[dict]:

        # ===== DEBUG =====
        db_name = self.db.execute(
            text("SELECT DB_NAME()")
        ).scalar()

        print("=" * 80)
        print("CURRENT DATABASE :", db_name)
        print("SQL :", sql)
        print("=" * 80)
        # =================

        result = self.db.execute(
            text(sql)
        )

        columns = result.keys()

        rows = result.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]