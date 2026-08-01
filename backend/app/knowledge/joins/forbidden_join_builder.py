from __future__ import annotations

from typing import Any

from app.knowledge.database_knowledge import DATABASE_KNOWLEDGE

__all__ = ["ForbiddenJoinBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 80
SECTION_TITLE = "FORBIDDEN JOINS"
FORBIDDEN_JOINS_TITLE = "Never Join With:"


class ForbiddenJoinBuilder:
    """
    Build the FORBIDDEN JOINS section.

    This builder explicitly tells the LLM which joins
    must never be generated for the selected tables.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the FORBIDDEN JOINS section.
        """

        context = [
            SECTION_SEPARATOR,
            "",
            SECTION_TITLE,
            "",
        ]

        for table_name in selected_tables:

            knowledge = DATABASE_KNOWLEDGE.get(table_name)

            if knowledge is None:
                continue

            forbidden_tables = knowledge.get(
                "forbidden_tables",
                (),
            )

            forbidden_lines = self._build_forbidden_lines(
                forbidden_tables,
                selected_tables,
            )

            if not forbidden_lines:
                continue

            context.extend(
                [
                    f"Table : {table_name}",
                    FORBIDDEN_JOINS_TITLE,
                    *forbidden_lines,
                    "",
                ]
            )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_forbidden_lines(
        self,
        forbidden_tables: tuple[str, ...] | list[str],
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the forbidden joins for one table.
        """

        lines: list[str] = []

        for table in forbidden_tables:

            if table not in selected_tables:
                continue

            lines.append(f"  - {table}")

        return lines