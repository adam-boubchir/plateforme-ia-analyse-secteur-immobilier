from app.services.metadata_service import (
    MetadataService,
)


class TableContextBuilder:
    """
    Build the tables section of the SQL context.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
    ):

        self.metadata_service = metadata_service

    def build(
        self,
    ) -> list[str]:
        """
        Build the tables section.
        """

        context = []

        context.append(
            "DATABASE TABLES"
        )

        context.append("")

        tables = (
            self.metadata_service.get_tables()
        )

        for table in tables:

            context.extend(
                self._build_table(
                    table
                )
            )

        context.append(
            "=" * 100
        )

        context.append("")

        return context

    def _build_table(
        self,
        table,
    ) -> list[str]:
        """
        Build one table description.
        """

        context = []

        context.append(
            f"TABLE : {table.table_name}"
        )

        if hasattr(
            table,
            "table_type",
        ):

            context.append(
                f"Type : {table.table_type}"
            )

        if hasattr(
            table,
            "row_count",
        ):

            context.append(
                f"Rows : {table.row_count}"
            )

        if hasattr(
            table,
            "is_fact_table",
        ):

            if table.is_fact_table:

                context.append(
                    "Category : FACT TABLE"
                )

            else:

                context.append(
                    "Category : DIMENSION TABLE"
                )

        context.append("Columns :")

        columns = (
            self.metadata_service.get_columns(
                table.table_name
            )
        )

        for column in columns:

            context.append(
                self._build_column(
                    column
                )
            )

        context.append("")

        return context

    def _build_column(
        self,
        column,
    ) -> str:
        """
        Build one column description.
        """

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

        length = ""

        if column.max_length:

            length = (
                f"({column.max_length})"
            )

        line = (
            f"  • {column.column_name}"
            f" : {column.data_type}"
            f"{length}"
            f"{flag_text}"
        )

        if column.semantic_type:

            line += (
                f" | Semantic={column.semantic_type}"
            )

        return line