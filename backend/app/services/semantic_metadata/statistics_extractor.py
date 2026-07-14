from sqlalchemy import text
from sqlalchemy.orm import Session


class StatisticsExtractor:
    """
    Extract statistics from one SQL column.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def extract(
        self,
        table_name: str,
        column_name: str,
        data_type: str,
    ) -> dict:

        result = {
            "min_value": None,
            "max_value": None,
            "distinct_count": 0,
        }

        try:

            query = text(f"""
                SELECT

                    COUNT(DISTINCT [{column_name}]) AS distinct_count,

                    MIN([{column_name}]) AS min_value,

                    MAX([{column_name}]) AS max_value

                FROM [{table_name}]
            """)

            row = self.db.execute(query).first()

            if row:

                result["distinct_count"] = row.distinct_count

                result["min_value"] = row.min_value

                result["max_value"] = row.max_value

        except Exception:

            pass

        return result