from sqlalchemy import text
from sqlalchemy.orm import Session


class SemanticKeywordRepository:
    """
    Repository used to retrieve semantic keywords.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_all(self) -> list[dict]:

        result = self.db.execute(
            text(
                """
                SELECT
                    keyword,
                    semantic_type,
                    score
                FROM SEMANTIC_KEYWORDS
                ORDER BY score DESC
                """
            )
        )

        return [

            {
                "keyword": row.keyword.lower(),
                "semantic_type": row.semantic_type,
                "score": row.score,
            }

            for row in result

        ]