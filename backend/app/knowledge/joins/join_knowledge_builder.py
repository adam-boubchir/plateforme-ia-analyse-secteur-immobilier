from app.knowledge.database_knowledge import (
    DATABASE_KNOWLEDGE,
)


class JoinKnowledgeBuilder:
    """
    Build the JOIN KNOWLEDGE section.

    This builder tells the LLM exactly how the selected
    tables are allowed to be joined.
    """

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the JOIN KNOWLEDGE section.
        """

        context = []

        context.append("=" * 80)
        context.append("")
        context.append("JOIN KNOWLEDGE")
        context.append("")

        for table_name in selected_tables:

            if table_name not in DATABASE_KNOWLEDGE:
                continue

            knowledge = DATABASE_KNOWLEDGE[
                table_name
            ]

            joins = knowledge.get(
                "joins",
                [],
            )

            if not joins:
                continue

            context.append(
                f"Table : {table_name}"
            )

            context.append(
                "Allowed Joins:"
            )

            for join in joins:

                target_table = join.get(
                    "target_table"
                )

                if (
                    target_table
                    not in selected_tables
                ):
                    continue

                context.append(

                    f"  - "
                    f"{table_name}.{join['source_column']} "
                    f"-> "
                    f"{target_table}.{join['target_column']}"

                )

            context.append("")

        return context