from __future__ import annotations

from typing import Any

from app.services.semantic_context_service import SemanticContextService

__all__ = ["SemanticContextBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 100

SECTION_TITLE = "SEMANTIC CONTEXT"
EXAMPLES_TITLE = "Examples :"


class SemanticContextBuilder:
    """
    Build the semantic context section of the SQL context.
    """

    def __init__(
        self,
        semantic_context_service: SemanticContextService,
    ) -> None:
        self.semantic_context_service = (
            semantic_context_service
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        question: str,
    ) -> list[str]:
        """
        Build the semantic context section.
        """

        semantic_columns = (
            self.semantic_context_service.build(
                question
            )
        )

        if not semantic_columns:
            return []

        context = [
            SECTION_TITLE,
            "",
        ]

        for column in semantic_columns:
            context.extend(
                self._build_column(
                    column,
                )
            )

        context.extend(
            [
                SECTION_SEPARATOR,
                "",
            ]
        )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_column(
        self,
        column: dict[str, Any],
    ) -> list[str]:
        """
        Build one semantic column description.
        """

        context = [
            f"TABLE : {column['table']}",
            f"COLUMN : {column['column']}",
        ]

        semantic_type = column.get(
            "semantic_type",
        )

        if semantic_type:
            context.append(
                f"Semantic Type : {semantic_type}"
            )

        examples = column.get(
            "examples",
        )

        if examples:
            context.extend(
                [
                    EXAMPLES_TITLE,
                    examples,
                ]
            )

        distinct_count = column.get(
            "distinct_count",
        )

        if distinct_count is not None:
            context.append(
                f"Distinct Values : {distinct_count}"
            )

        min_value = column.get(
            "min_value",
        )

        max_value = column.get(
            "max_value",
        )

        if (
            min_value is not None
            or max_value is not None
        ):
            context.append(
                f"Range : {min_value} -> {max_value}"
            )

        if column.get(
            "is_primary_key",
        ):
            context.append(
                "Primary Key : YES"
            )

        if column.get(
            "is_foreign_key",
        ):
            context.append(
                "Foreign Key : YES"
            )

        score = column.get(
            "score",
        )

        if score is not None:
            context.append(
                f"Semantic Score : {score}"
            )

        context.append("")

        return context