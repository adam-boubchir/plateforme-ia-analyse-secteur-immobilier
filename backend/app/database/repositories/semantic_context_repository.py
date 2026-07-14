from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


class SemanticContextRepository(BaseRepository):
    """
    Repository used to retrieve the most relevant columns
    for a natural language question.
    """

    MAX_RESULTS = 15

    def search(
        self,
        keywords: list[str],
    ) -> list[ColumnMetadataEntity]:

        if not keywords:
            return []

        columns = (
            self.db.query(
                ColumnMetadataEntity
            )
            .filter(
                ColumnMetadataEntity.is_searchable == True
            )
            .all()
        )

        scored_columns = []

        for column in columns:

            score = self._compute_score(
                column,
                keywords,
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

            for score, column in scored_columns[
                : self.MAX_RESULTS
            ]

        ]

    def _compute_score(
        self,
        column: ColumnMetadataEntity,
        keywords: list[str],
    ) -> int:

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

            # colonne
            if keyword == column_name:
                score += 120

            elif keyword in column_name:
                score += 90

            # semantic type
            if keyword == semantic_type:
                score += 100

            elif keyword in semantic_type:
                score += 80

            # table
            if keyword == table_name:
                score += 70

            elif keyword in table_name:
                score += 50

            # exemples
            if keyword in examples:
                score += 60

            # description
            if keyword in description:
                score += 30

        # Bonus métier

        if column.semantic_type == "MEASURE":
            score += 15

        elif column.semantic_type in (
            "REGION",
            "PROVINCE",
            "COMMUNE",
            "TIME",
        ):
            score += 10

        # Bonus FK

        if column.is_foreign_key:
            score += 8

        # Bonus PK

        if column.is_primary_key:
            score += 5

        return score