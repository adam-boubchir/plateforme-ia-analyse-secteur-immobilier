from sqlalchemy import text
from sqlalchemy.orm import Session


class ExampleValueExtractor:
    """
    Extract representative values from one column.
    """

    MAX_EXAMPLES = 20

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
    ) -> str:

        if not self._is_text_column(data_type):
            return ""

        try:

            query = text(
                f"""
                SELECT DISTINCT TOP ({self.MAX_EXAMPLES})
                    [{column_name}]
                FROM [{table_name}]
                WHERE [{column_name}] IS NOT NULL
                ORDER BY [{column_name}]
                """
            )

            result = self.db.execute(query)

            values = []

            for row in result:

                value = row[0]

                if value is None:
                    continue

                value = str(value).strip()

                if value == "":
                    continue

                values.append(value)

            return " | ".join(values)

        except Exception:

            return ""

    def _is_text_column(
        self,
        data_type: str,
    ) -> bool:

        data_type = data_type.lower()

        return any(
            t in data_type
            for t in [
                "char",
                "varchar",
                "nvarchar",
                "text",
                "ntext",
            ]
        )