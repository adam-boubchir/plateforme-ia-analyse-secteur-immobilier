import re
from typing import Any

from app.database.entities.column_metadata import ColumnMetadataEntity
from app.database.entities.table_metadata import TableMetadataEntity
from app.database.entities.relationship import RelationshipEntity
from app.database.repositories.semantic_context_repository import (
    SemanticContextRepository,
)

# ==========================================================
# CONSTANTS
# ==========================================================

STOP_WORDS: set[str] = {
    "le",
    "la",
    "les",
    "de",
    "des",
    "du",
    "dans",
    "sur",
    "sous",
    "pour",
    "par",
    "avec",
    "sans",
    "et",
    "ou",
    "un",
    "une",
    "est",
    "sont",
    "quel",
    "quelle",
    "quels",
    "quelles",
    "donne",
    "donner",
    "montre",
    "affiche",
    "liste",
    "voir",
    "afficher",
    "peux",
    "peut",
    "avoir",
    "faire",
    "tous",
    "toutes",
    "entre",
    "vers",
    "chez",
    "plus",
    "moins",
    "combien",
    "moi",
}

WORD_PATTERN = re.compile(
    r"[a-zA-ZÀ-ÿ0-9]+"
)


class SemanticContextService:
    """
    Service responsible for retrieving the semantic
    database context associated with a user question.
    """

    def __init__(
        self,
        repository: SemanticContextRepository,
    ) -> None:

        self.repository: SemanticContextRepository = (
            repository
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        question: str,
    ) -> list[dict[str, Any]]:
        """
        Build the semantic context used by the SQL Agent.
        """

        keywords: list[str] = self._extract_keywords(
            question=question,
        )

        columns: list[ColumnMetadataEntity] = (
            self.repository.search(
                keywords=keywords,
            )
        )

        return [
            self._build_context_item(
                column=column,
            )
            for column in columns
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_context_item(
        self,
        column: ColumnMetadataEntity,
    ) -> dict[str, Any]:
        """
        Build one semantic context item.
        """

        return {
            "table": column.table_name,
            "column": column.column_name,
            "semantic_type": column.semantic_type,
            "examples": column.example_values,
            "min_value": column.min_value,
            "max_value": column.max_value,
            "distinct_count": column.distinct_count,
            "is_primary_key": column.is_primary_key,
            "is_foreign_key": column.is_foreign_key,
            "score": getattr(
                column,
                "semantic_score",
                None,
            ),
        }

    def _extract_keywords(
        self,
        question: str,
    ) -> list[str]:
        """
        Extract meaningful keywords from
        a natural language question.
        """

        words: list[str] = WORD_PATTERN.findall(
            question.lower(),
        )

        keywords: list[str] = []

        for word in words:

            word = word.strip()

            if len(word) < 2:
                continue

            if word in STOP_WORDS:
                continue

            keywords.append(word)

        return list(
            dict.fromkeys(
                keywords,
            )
        )


__all__ = [
    "SemanticContextService",
]