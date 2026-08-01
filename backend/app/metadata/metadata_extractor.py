from __future__ import annotations

from typing import Final

from sqlalchemy import text
from sqlalchemy.engine import CursorResult

from app.database.connection_ministry import engine_ministry
from app.database.session import SessionLocal
from app.metadata.metadata_loader import MetadataLoader
from app.metadata.metadata_models import (
    ColumnMetadata,
    MetadataLoadResult,
    RelationshipMetadata,
    TableMetadata,
)

__all__ = ["MetadataExtractor"]

FOREIGN_KEY_RELATIONSHIP: Final[str] = "FOREIGN_KEY"

TABLES_QUERY = text("""
SELECT
    TABLE_CATALOG,
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
""")

COLUMNS_QUERY = text("""
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_NAME, ORDINAL_POSITION
""")

RELATIONSHIPS_QUERY = text("""
SELECT
    fk.name AS FK_NAME,

    tp.name AS SOURCE_TABLE,
    cp.name AS SOURCE_COLUMN,

    tr.name AS TARGET_TABLE,
    cr.name AS TARGET_COLUMN

FROM sys.foreign_keys fk

INNER JOIN sys.foreign_key_columns fkc
    ON fk.object_id = fkc.constraint_object_id

INNER JOIN sys.tables tp
    ON fkc.parent_object_id = tp.object_id

INNER JOIN sys.columns cp
    ON fkc.parent_object_id = cp.object_id
    AND fkc.parent_column_id = cp.column_id

INNER JOIN sys.tables tr
    ON fkc.referenced_object_id = tr.object_id

INNER JOIN sys.columns cr
    ON fkc.referenced_object_id = cr.object_id
    AND fkc.referenced_column_id = cr.column_id
""")


class MetadataExtractor:

    def __init__(self) -> None:
        self.engine = engine_ministry

    def _execute(self, query) -> CursorResult:
        with self.engine.connect() as connection:
            return connection.execute(query)

    def extract_tables(self) -> list[TableMetadata]:
        result = self._execute(TABLES_QUERY)

        return [
            TableMetadata(
                source_database=row.TABLE_CATALOG,
                schema_name=row.TABLE_SCHEMA,
                table_name=row.TABLE_NAME,
            )
            for row in result
        ]

    def extract_columns(self) -> list[ColumnMetadata]:
        result = self._execute(COLUMNS_QUERY)

        return [
            ColumnMetadata(
                table_name=row.TABLE_NAME,
                column_name=row.COLUMN_NAME,
                data_type=row.DATA_TYPE,
                is_nullable=(row.IS_NULLABLE == "YES"),
                is_primary_key=False,
                is_foreign_key=False,
                sample_values=None,
                business_name=None,
                description=None,
            )
            for row in result
        ]

    def extract_relationships(self) -> list[RelationshipMetadata]:
        result = self._execute(RELATIONSHIPS_QUERY)

        return [
            RelationshipMetadata(
                source_table=row.SOURCE_TABLE,
                source_column=row.SOURCE_COLUMN,
                target_table=row.TARGET_TABLE,
                target_column=row.TARGET_COLUMN,
                relationship_type=FOREIGN_KEY_RELATIONSHIP,
            )
            for row in result
        ]

    def run(self) -> MetadataLoadResult:
        db = SessionLocal()

        try:
            loader = MetadataLoader(db)

            result = MetadataLoadResult()

            result.merge(
                loader.save_tables(
                    self.extract_tables()
                )
            )

            result.merge(
                loader.save_columns(
                    self.extract_columns()
                )
            )

            result.merge(
                loader.save_relationships(
                    self.extract_relationships()
                )
            )

            loader.create_log(result)

            return result

        finally:
            db.close()