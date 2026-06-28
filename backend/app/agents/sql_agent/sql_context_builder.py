from app.services.metadata_service import MetadataService


class SQLContextBuilder:
    """
    Build the database context that will be sent to the LLM.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
    ):

        self.metadata_service = metadata_service

    def build_context(self) -> str:
        """
        Build the complete SQL context.
        """

        context = []

        context.extend(
            self._build_header()
        )

        context.extend(
            self._build_tables_section()
        )

        context.extend(
            self._build_relationships_section()
        )

        return "\n".join(context)

    def _build_header(
        self,
    ) -> list[str]:
        """
        Build the header section.
        """

        return [
            "DATABASE : OBSERVATOIRE_STAGIAIRE",
            "",
            "=" * 80,
            "",
        ]

    def _build_tables_section(
        self,
    ) -> list[str]:
        """
        Build the tables section.
        """

        context = []

        tables = self.metadata_service.get_tables()

        context.append("TABLES")
        context.append("")

        for table in tables:

            context.append(
                f"Table : {table.schema_name}.{table.table_name}"
            )

            if hasattr(table, "table_type"):
                context.append(
                    f"Type : {table.table_type}"
                )

            if hasattr(table, "row_count"):
                context.append(
                    f"Rows : {table.row_count}"
                )

            if hasattr(table, "is_fact_table"):

                if table.is_fact_table:
                    context.append(
                        "Category : FACT TABLE"
                    )
                else:
                    context.append(
                        "Category : DIMENSION TABLE"
                    )

            context.append("Columns:")

            columns = self.metadata_service.get_columns(
                table.table_name
            )

            for column in columns:

                flags = []

                if column.is_primary_key:
                    flags.append("PK")

                if column.is_foreign_key:
                    flags.append("FK")

                flag_text = ""

                if flags:

                    flag_text = (
                        " ["
                        + ", ".join(flags)
                        + "]"
                    )

                max_length = ""

                if column.max_length is not None:

                    max_length = (
                        f"({column.max_length})"
                    )

                context.append(
                    f"  - {column.column_name}"
                    f" : {column.data_type}"
                    f"{max_length}"
                    f"{flag_text}"
                )

            context.append("")

        return context

    def _build_relationships_section(
        self,
    ) -> list[str]:
        """
        Build the relationships section.
        """

        context = []

        relationships = (
            self.metadata_service.get_relationships()
        )

        context.append("=" * 80)
        context.append("")
        context.append("RELATIONSHIPS")
        context.append("")

        for relation in relationships:

            if hasattr(relation, "constraint_name"):

                context.append(
                    f"Constraint : {relation.constraint_name}"
                )

            context.append(
                f"{relation.source_table}.{relation.source_column}"
            )

            context.append("    ↓")

            context.append(
                f"{relation.target_table}.{relation.target_column}"
            )

            context.append("")

        return context