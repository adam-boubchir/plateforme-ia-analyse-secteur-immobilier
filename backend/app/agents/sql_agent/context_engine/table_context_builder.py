from __future__ import annotations

from typing import Any

from app.services.metadata_service import MetadataService

__all__ = ("TableContextBuilder",)

# ==========================================================
# CONSTANTS
# ==========================================================

_SECTION_SEPARATOR = "=" * 100
_SECTION_TITLE = "DATABASE TABLES"
_COLUMN_TITLE = "Columns:"


class TableContextBuilder:
    """
    Build the database tables section of the SQL context.

    Only the selected tables are included in the generated context.
    """

    def __init__(
        self,
        *,
        metadata_service: MetadataService,
    ) -> None:
        self._metadata_service = metadata_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the database tables section.
        """

        context = [
            _SECTION_TITLE,
            "",
        ]

        for table in self._get_selected_tables(
            selected_tables=selected_tables,
        ):
            context.extend(
                self._build_table(
                    table=table,
                )
            )

        context.extend(
            (
                _SECTION_SEPARATOR,
                "",
            )
        )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_selected_tables(
        self,
        *,
        selected_tables: list[str],
    ) -> list[Any]:
        """
        Return the metadata of the selected tables.
        """

        return [
            table
            for table in self._metadata_service.get_tables()
            if table.table_name in selected_tables
        ]

    def _build_table(
        self,
        *,
        table: Any,
    ) -> list[str]:
        """
        Build one table description.
        """

        return [
            f"TABLE : {table.table_name}",
            *self._build_table_metadata(
                table=table,
            ),
            _COLUMN_TITLE,
            *self._build_columns(
                columns=self._metadata_service.get_columns(
                    table_name=table.table_name,
                ),
            ),
            "",
        ]

    @staticmethod
    def _build_table_metadata(
        *,
        table: Any,
    ) -> list[str]:
        """
        Build metadata describing one table.
        """

        metadata: list[str] = []

        if hasattr(
            table,
            "table_type",
        ):
            metadata.append(
                f"Type : {table.table_type}"
            )

        if hasattr(
            table,
            "row_count",
        ):
            metadata.append(
                f"Rows : {table.row_count}"
            )

        if hasattr(
            table,
            "is_fact_table",
        ):
            metadata.append(
                "Category : FACT TABLE"
                if table.is_fact_table
                else "Category : DIMENSION TABLE"
            )

        return metadata

    def _build_columns(
        self,
        *,
        columns: list[Any],
    ) -> list[str]:
        """
        Build all column descriptions.
        """

        return [
            self._build_column(
                column=column,
            )
            for column in columns
        ]

    @staticmethod
    def _build_column(
        *,
        column: Any,
    ) -> str:
        """
        Build one column description.
        """

        flags: list[str] = []

        if column.is_primary_key:
            flags.append("PK")

        if column.is_foreign_key:
            flags.append("FK")

        flag_text = (
            f" [{', '.join(flags)}]"
            if flags
            else ""
        )

        length = (
            f"({column.max_length})"
            if column.max_length
            else ""
        )

        line = (
            f"  • {column.column_name}"
            f" : {column.data_type}"
            f"{length}"
            f"{flag_text}"
        )

        semantic_type = getattr(
            column,
            "semantic_type",
            None,
        )

        if semantic_type:
            line += (
                f" | Semantic={semantic_type}"
            )

        return line