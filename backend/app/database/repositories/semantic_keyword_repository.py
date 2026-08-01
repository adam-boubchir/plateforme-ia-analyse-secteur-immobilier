from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session


class SemanticKeywordRepository:
    """
    Repository responsible for retrieving semantic keywords.
    """

    GET_ALL_QUERY = text(
        """
        SELECT
            keyword,
            semantic_type,
            score
        FROM SEMANTIC_KEYWORDS
        ORDER BY score DESC
        """
    )

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db: Session = db

    # ==========================================================
    # READ
    # ==========================================================

    def get_all(
        self,
    ) -> list[dict[str, str | int]]:
        """
        Retrieve every semantic keyword ordered by score.
        """

        result = self.db.execute(
            statement=self.GET_ALL_QUERY,
        )

        rows: list[RowMapping] = result.mappings().all()

        return [
            {
                "keyword": row["keyword"].lower(),
                "semantic_type": row["semantic_type"],
                "score": row["score"],
            }
            for row in rows
        ]


__all__ = [
    "SemanticKeywordRepository",
]