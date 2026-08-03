from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)

__all__ = (
    "SemanticContextRepository",
)


class SemanticContextRepository(BaseRepository):
    """
    Repository used to retrieve the most relevant columns
    for a natural-language question.
    """

    _MAX_RESULTS = 15

    _EXACT_COLUMN_SCORE = 120
    _PARTIAL_COLUMN_SCORE = 90

    _EXACT_SEMANTIC_SCORE = 100
    _PARTIAL_SEMANTIC_SCORE = 80

    _EXACT_TABLE_SCORE = 70
    _PARTIAL_TABLE_SCORE = 50

    _EXAMPLE_SCORE = 60
    _DESCRIPTION_SCORE = 30

    _MEASURE_BONUS = 15
    _LOCATION_BONUS = 10

    _FOREIGN_KEY_BONUS = 8
    _PRIMARY_KEY_BONUS = 5

    _LOCATION_TYPES = frozenset(
        {
            "REGION",
            "PROVINCE",
            "COMMUNE",
            "TIME",
        }
    )

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def search(
        self,
        *,
        keywords: list[str],
    ) -> list[ColumnMetadataEntity]:
        """
        Retrieve the most relevant searchable columns.

        Args:
            keywords:
                Extracted keywords from the user question.

        Returns:
            Ranked list of matching columns.
        """

        if not keywords:
            return []

        statement = (
            select(
                ColumnMetadataEntity,
            )
            .where(
                (
                    ColumnMetadataEntity.is_searchable
                    == True
                ),
            )
        )

        columns = list(
            self._db.scalars(
                statement,
            )
        )

        scored_columns: list[
            tuple[int, ColumnMetadataEntity]
        ] = []

        for column in columns:
            score = self._compute_score(
                column=column,
                keywords=keywords,
            )

            if score <= 0:
                continue

            scored_columns.append(
                (
                    score,
                    column,
                )
            )

        scored_columns.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        ranked_columns = [
            column
            for _, column in scored_columns[
                : self._MAX_RESULTS
            ]
        ]

        return ranked_columns

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _compute_score(
        self,
        *,
        column: ColumnMetadataEntity,
        keywords: list[str],
    ) -> int:
        """
        Compute the semantic relevance score of one column.

        Args:
            column:
                Metadata column.

            keywords:
                Extracted keywords.

        Returns:
            Relevance score.
        """

        score = 0

        table_name = (
            column.table_name or ""
        ).lower()

        column_name = (
            column.column_name or ""
        ).lower()

        semantic_type = (
            column.semantic_type or ""
        ).lower()

        examples = (
            column.example_values or ""
        ).lower()

        description = (
            column.description or ""
        ).lower()

        for keyword in keywords:
            keyword = keyword.lower()

            if keyword == column_name:
                score += self._EXACT_COLUMN_SCORE

            elif keyword in column_name:
                score += self._PARTIAL_COLUMN_SCORE

            if keyword == semantic_type:
                score += self._EXACT_SEMANTIC_SCORE

            elif keyword in semantic_type:
                score += self._PARTIAL_SEMANTIC_SCORE

            if keyword == table_name:
                score += self._EXACT_TABLE_SCORE

            elif keyword in table_name:
                score += self._PARTIAL_TABLE_SCORE

            if keyword in examples:
                score += self._EXAMPLE_SCORE

            if keyword in description:
                score += self._DESCRIPTION_SCORE

        semantic_type_upper = (
            column.semantic_type or ""
        ).upper()

        if semantic_type_upper == "MEASURE":
            score += self._MEASURE_BONUS

        elif semantic_type_upper in self._LOCATION_TYPES:
            score += self._LOCATION_BONUS

        if column.is_foreign_key:
            score += self._FOREIGN_KEY_BONUS

        if column.is_primary_key:
            score += self._PRIMARY_KEY_BONUS

        return score