from __future__ import annotations

from typing import Any

from app.knowledge.database_knowledge import DATABASE_KNOWLEDGE

__all__ = ["JoinKnowledgeBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 80
SECTION_TITLE = "JOIN KNOWLEDGE"
ALLOWED_JOINS_TITLE = "Allowed Joins:"


class JoinKnowledgeBuilder:
    """
    Build the JOIN KNOWLEDGE section.

    This builder tells the LLM exactly how the selected
    tables are allowed to be joined.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the JOIN KNOWLEDGE section.
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

            joins = knowledge.get("joins", ())

            if not joins:
                continue

            join_lines = self._build_join_lines(
                table_name,
                joins,
                selected_tables,
            )

            if not join_lines:
                continue

            context.extend(
                [
                    f"Table : {table_name}",
                    ALLOWED_JOINS_TITLE,
                    *join_lines,
                    "",
                ]
            )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_join_lines(
        self,
        table_name: str,
        joins: tuple[dict[str, Any], ...] | list[dict[str, Any]],
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build all allowed joins for one table.
        """

        lines: list[str] = []

        for join in joins:

            target_table = join.get("target_table")

            if target_table not in selected_tables:
                continue

            lines.append(
                f"  - "
                f"{table_name}.{join['source_column']} "
                f"-> "
                f"{target_table}.{join['target_column']}"
            )

        return lines