from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session

__all__ = [
    "SemanticKeywordRepository",
]


class SemanticKeywordRepository:
    """
    Repository responsible for retrieving semantic keywords.
    """

    _GET_ALL_QUERY = text(
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
        self._db = db

    # ==========================================================
    # READ
    # ==========================================================

    def get_all(
        self,
    ) -> list[dict[str, Any]]:
        """
        Retrieve every semantic keyword ordered by score.
        """

        result = self._db.execute(
            statement=self._GET_ALL_QUERY,
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