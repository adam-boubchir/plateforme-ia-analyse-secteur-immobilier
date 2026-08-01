from __future__ import annotations

from typing import Any

from app.services.metadata_service import MetadataService

__all__ = ["RelationshipContextBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 100

SECTION_TITLE = "DATABASE RELATIONSHIPS"

EMPTY_RELATIONSHIPS_MESSAGE = "No relationships found."


class RelationshipContextBuilder:
    """
    Build the database relationships section of the SQL context.

    Only relationships involving the selected tables
    are included in the generated context.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
    ) -> None:
        self.metadata_service = metadata_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the relationships section.
        """

        relationships = self._get_selected_relationships(
            selected_tables,
        )

        context = [
            SECTION_TITLE,
            "",
        ]

        if relationships:

            for relationship in relationships:
                context.extend(
                    self._build_relationship(
                        relationship,
                    )
                )

        else:

            context.extend(
                self._empty_relationships(),
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

    def _get_selected_relationships(
        self,
        selected_tables: list[str],
    ) -> list[Any]:
        """
        Return only the relationships involving
        the selected tables.
        """

        return [
            relationship
            for relationship in self.metadata_service.get_relationships()
            if (
                relationship.source_table in selected_tables
                and relationship.target_table in selected_tables
            )
        ]

    def _empty_relationships(
        self,
    ) -> list[str]:
        """
        Build the empty relationships section.
        """

        return [
            EMPTY_RELATIONSHIPS_MESSAGE,
            "",
        ]

    def _build_relationship(
        self,
        relationship: Any,
    ) -> list[str]:
        """
        Build one relationship description.
        """

        context: list[str] = []

        constraint = getattr(
            relationship,
            "constraint_name",
            None,
        )

        if constraint:

            context.append(
                f"Constraint : {constraint}"
            )

        context.extend(
            [
                (
                    f"{relationship.source_table}"
                    f".{relationship.source_column}"
                ),
                "        ↓",
                (
                    f"{relationship.target_table}"
                    f".{relationship.target_column}"
                ),
                "",
            ]
        )

        return context