from __future__ import annotations

from typing import Any

from app.knowledge.database_knowledge import DATABASE_KNOWLEDGE

__all__ = ["BusinessKnowledgeBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 80
SECTION_TITLE = "BUSINESS KNOWLEDGE"

USED_FOR_TITLE = "Used For:"
NEVER_USE_FOR_TITLE = "Never Use For:"
IMPORTANT_COLUMNS_TITLE = "Important Columns:"


class BusinessKnowledgeBuilder:
    """
    Build the Business Knowledge section of the SQL prompt.

    This builder converts the business knowledge catalog into
    a human-readable context that helps the LLM understand
    the role of every selected table.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the Business Knowledge section using only
        the selected tables.
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

            context.extend(
                self._build_table_context(
                    table_name,
                    knowledge,
                )
            )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_table_context(
        self,
        table_name: str,
        knowledge: dict[str, Any],
    ) -> list[str]:
        """
        Build the business description of one table.
        """

        context = [
            f"Table : {table_name}",
            f"Business Name : {knowledge['business_name']}",
            f"Description : {knowledge['description']}",
        ]

        self._append_section(
            context,
            USED_FOR_TITLE,
            knowledge.get("used_for", ()),
        )

        self._append_section(
            context,
            NEVER_USE_FOR_TITLE,
            knowledge.get("never_use_for", ()),
        )

        self._append_section(
            context,
            IMPORTANT_COLUMNS_TITLE,
            knowledge.get("main_columns", ()),
        )

        context.append("")

        return context

    def _append_section(
        self,
        context: list[str],
        title: str,
        values: tuple[str, ...] | list[str],
    ) -> None:
        """
        Append a titled bullet-list section.
        """

        if not values:
            return

        context.append(title)

        for value in values:
            context.append(f"  - {value}")