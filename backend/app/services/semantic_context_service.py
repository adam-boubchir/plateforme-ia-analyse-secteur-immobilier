from __future__ import annotations

import re
from typing import Any

from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)
from app.database.repositories.semantic_context_repository import (
    SemanticContextRepository,
)

__all__ = (
    "SemanticContextService",
)

# ==========================================================
# CONSTANTS
# ==========================================================

_STOP_WORDS: frozenset[str] = frozenset(
    {
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
)

_WORD_PATTERN = re.compile(
    r"[a-zA-ZÀ-ÿ0-9]+",
)


class SemanticContextService:
    """
    Retrieve the semantic database context associated with a
    natural-language question.
    """

    def __init__(
        self,
        *,
        repository: SemanticContextRepository,
    ) -> None:
        self._repository = repository

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        question: str,
    ) -> list[dict[str, Any]]:
        """
        Build the semantic context used by the SQL Agent.

        Args:
            question:
                User natural-language question.

        Returns:
            List of semantic context items.
        """

        keywords = self._extract_keywords(
            question=question,
        )

        columns = self._repository.search(
            keywords=keywords,
        )

        context_items = [
            self._build_context_item(
                column=column,
            )
            for column in columns
        ]

        return context_items

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_context_item(
        *,
        column: ColumnMetadataEntity,
    ) -> dict[str, Any]:
        """
        Convert one metadata entity into a semantic context item.

        Args:
            column:
                Column metadata entity.

        Returns:
            Dictionary consumed by the SemanticContextBuilder.
        """

        context_item = {
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

        return context_item

    @staticmethod
    def _extract_keywords(
        *,
        question: str,
    ) -> list[str]:
        """
        Extract meaningful keywords from a natural-language question.

        Args:
            question:
                User question.

        Returns:
            Ordered list of unique keywords.
        """

        words = _WORD_PATTERN.findall(
            question.casefold(),
        )

        keywords: list[str] = []

        for word in words:
            word = word.strip()

            if len(word) < 2:
                continue

            if word in _STOP_WORDS:
                continue

            keywords.append(
                word,
            )

        unique_keywords = list(
            dict.fromkeys(
                keywords,
            )
        )

        return unique_keywords