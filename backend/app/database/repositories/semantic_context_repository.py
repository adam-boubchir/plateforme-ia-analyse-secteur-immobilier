from __future__ import annotations

from sqlalchemy import select

from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)

__all__ = [
    "SemanticContextRepository",
]


class SemanticContextRepository(BaseRepository):
    """
    Repository used to retrieve the most relevant columns
    for a natural language question.
    """

    MAX_RESULTS = 15

    EXACT_COLUMN_SCORE = 120
    PARTIAL_COLUMN_SCORE = 90

    EXACT_SEMANTIC_SCORE = 100
    PARTIAL_SEMANTIC_SCORE = 80

    EXACT_TABLE_SCORE = 70
    PARTIAL_TABLE_SCORE = 50

    EXAMPLE_SCORE = 60
    DESCRIPTION_SCORE = 30

    MEASURE_BONUS = 15
    LOCATION_BONUS = 10

    FOREIGN_KEY_BONUS = 8
    PRIMARY_KEY_BONUS = 5

    LOCATION_TYPES = {
        "REGION",
        "PROVINCE",
        "COMMUNE",
        "TIME",
    }

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def search(
        self,
        keywords: list[str],
    ) -> list[ColumnMetadataEntity]:
        """
        Return the most relevant searchable columns.
        """

        if not keywords:
            return []

        statement = (
            select(
                ColumnMetadataEntity,
            )
            .where(
                ColumnMetadataEntity.is_searchable == True
            )
        )

        columns = list(
            self.db.scalars(
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

        return [
            column
            for _, column in scored_columns[
                : self.MAX_RESULTS
            ]
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _compute_score(
        self,
        column: ColumnMetadataEntity,
        keywords: list[str],
    ) -> int:
        """
        Compute a relevance score for one column.
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
                score += self.EXACT_COLUMN_SCORE

            elif keyword in column_name:
                score += self.PARTIAL_COLUMN_SCORE

            if keyword == semantic_type:
                score += self.EXACT_SEMANTIC_SCORE

            elif keyword in semantic_type:
                score += self.PARTIAL_SEMANTIC_SCORE

            if keyword == table_name:
                score += self.EXACT_TABLE_SCORE

            elif keyword in table_name:
                score += self.PARTIAL_TABLE_SCORE

            if keyword in examples:
                score += self.EXAMPLE_SCORE

            if keyword in description:
                score += self.DESCRIPTION_SCORE

        semantic_type_upper = (
            column.semantic_type or ""
        ).upper()

        if semantic_type_upper == "MEASURE":
            score += self.MEASURE_BONUS

        elif semantic_type_upper in self.LOCATION_TYPES:
            score += self.LOCATION_BONUS

        if column.is_foreign_key:
            score += self.FOREIGN_KEY_BONUS

        if column.is_primary_key:
            score += self.PRIMARY_KEY_BONUS

        return score