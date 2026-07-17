from app.knowledge.database_knowledge import (
    DATABASE_KNOWLEDGE,
)


class ForbiddenJoinBuilder:
    """
    Build the FORBIDDEN JOINS section.

    This builder explicitly tells the LLM which joins
    must never be generated for the selected tables.
    """

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the FORBIDDEN JOINS section.
        """

        context = []

        context.append("=" * 80)
        context.append("")
        context.append("FORBIDDEN JOINS")
        context.append("")

        for table_name in selected_tables:

            if table_name not in DATABASE_KNOWLEDGE:
                continue

            knowledge = DATABASE_KNOWLEDGE[
                table_name
            ]

            forbidden_tables = knowledge.get(
                "forbidden_tables",
                [],
            )

            if not forbidden_tables:
                continue

            context.append(
                f"Table : {table_name}"
            )

            context.append(
                "Never Join With:"
            )

            for forbidden_table in forbidden_tables:

                if (
                    forbidden_table
                    not in selected_tables
                ):
                    continue

                context.append(
                    f"  - {forbidden_table}"
                )

            context.append("")

        return context