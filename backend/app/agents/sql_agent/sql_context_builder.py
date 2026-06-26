from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.entities.table_metadata import (
    TableMetadataEntity
)

from app.database.entities.column_metadata import (
    ColumnMetadataEntity
)

from app.database.entities.relationship import (
    RelationshipEntity
)


class SQLContextBuilder:

    def __init__(self, db: Session):
        self.db = db

    def build_context(self) -> str:

        tables = self.db.scalars(
            select(TableMetadataEntity)
            .order_by(TableMetadataEntity.table_name)
        ).all()

        columns = self.db.scalars(
            select(ColumnMetadataEntity)
            .order_by(
                ColumnMetadataEntity.table_name,
                ColumnMetadataEntity.column_name
            )
        ).all()

        relationships = self.db.scalars(
            select(RelationshipEntity)
        ).all()

        context = []

        context.append(
            "DATABASE schema_name"
        )

        context.append("")

        for table in tables:

            context.append(
                f"Table: {table.table_name}"
            )

            table_columns = [

                column

                for column in columns

                if column.table_name == table.table_name

            ]

            context.append("Columns:")

            for column in table_columns:

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

                context.append(
                    f"- {column.column_name} "
                    f"({column.data_type})"
                    f"{flag_text}"
                )

            context.append("")

        if relationships:

            context.append("RELATIONSHIPS")

            context.append("")

            for relation in relationships:

                context.append(
                    f"{relation.source_table}."
                    f"{relation.source_column}"
                    f" -> "
                    f"{relation.target_table}."
                    f"{relation.target_column}"
                )

        return "\n".join(context)