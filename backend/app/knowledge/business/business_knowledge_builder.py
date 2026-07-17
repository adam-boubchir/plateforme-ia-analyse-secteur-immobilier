from app.knowledge.database_knowledge import (
    DATABASE_KNOWLEDGE,
)


class BusinessKnowledgeBuilder:
    """
    Build the Business Knowledge section of the SQL prompt.

    This builder converts the business knowledge catalog into
    a human-readable context that helps the LLM understand
    the role of every selected table.
    """

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the Business Knowledge section using only
        the selected tables.
        """

        context = []

        context.append("=" * 80)
        context.append("")
        context.append("BUSINESS KNOWLEDGE")
        context.append("")

        for table_name in selected_tables:

            if table_name not in DATABASE_KNOWLEDGE:
                continue

            knowledge = DATABASE_KNOWLEDGE[
                table_name
            ]

            context.extend(
                self._build_table_context(
                    table_name,
                    knowledge,
                )
            )

        return context

    def _build_table_context(
        self,
        table_name: str,
        knowledge: dict,
    ) -> list[str]:
        """
        Build the business description of one table.
        """

        context = []

        context.append(f"Table : {table_name}")

        context.append(
            f"Business Name : {knowledge['business_name']}"
        )

        context.append(
            f"Description : {knowledge['description']}"
        )

        used_for = knowledge.get(
            "used_for",
            [],
        )

        if used_for:

            context.append("Used For:")

            for value in used_for:

                context.append(
                    f"  - {value}"
                )

        never_use_for = knowledge.get(
            "never_use_for",
            [],
        )

        if never_use_for:

            context.append("Never Use For:")

            for value in never_use_for:

                context.append(
                    f"  - {value}"
                )

        main_columns = knowledge.get(
            "main_columns",
            [],
        )

        if main_columns:

            context.append(
                "Important Columns:"
            )

            for column in main_columns:

                context.append(
                    f"  - {column}"
                )

        context.append("")

        return context