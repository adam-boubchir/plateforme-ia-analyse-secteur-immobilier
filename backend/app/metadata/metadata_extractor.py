from sqlalchemy import text

from app.metadata.metadata_models import (
    TableMetadata,
    ColumnMetadata,
    RelationshipMetadata,
    MetadataLoadResult
)

from app.database.connection_ministry import (
    engine_ministry
)

from app.metadata.metadata_loader import (
    MetadataLoader
)

from app.database.session import SessionLocal

class MetadataExtractor:

    def __init__(self):
        self.engine = engine_ministry

    def extract_tables(self) -> list[TableMetadata]:
        query = text("""
            SELECT
                TABLE_CATALOG,
                TABLE_schema_name,
                TABLE_NAME
            FROM INFORMATION_schema_name.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)

        tables = []

        with self.engine.connect() as connection:

            result = connection.execute(query)

            for row in result:

                tables.append(
                    TableMetadata(
                        source_database=row.TABLE_CATALOG,
                        schema_name_name=row.TABLE_schema_name,
                        table_name=row.TABLE_NAME
                    )
                )

        return tables
    
    def extract_columns(self) -> list[ColumnMetadata]:
        query = text("""
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE
            FROM INFORMATION_schema_name.COLUMNS
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """)

        columns = []

        with self.engine.connect() as connection:

            result = connection.execute(query)

            for row in result:

                columns.append(
                    ColumnMetadata(
                        table_name=row.TABLE_NAME,
                        column_name=row.COLUMN_NAME,
                        data_type=row.DATA_TYPE,
                        is_nullable=(
                            row.IS_NULLABLE == "YES"
                        ),
                        is_primary_key=False,
                        is_foreign_key=False,
                        sample_values=None,
                        business_name=None,
                        description=None
                    )
                )

        return columns
    def extract_relationships(
        self
    ) -> list[RelationshipMetadata]:
        query = text("""
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

        relationships = []

        with self.engine.connect() as connection:

            result = connection.execute(query)

            for row in result:

                relationships.append(
                    RelationshipMetadata(
                        source_table=row.SOURCE_TABLE,
                        source_column=row.SOURCE_COLUMN,
                        target_table=row.TARGET_TABLE,
                        target_column=row.TARGET_COLUMN,
                        relationship_type="FOREIGN_KEY"
                    )
                )

        return relationships
    
    def run(self) -> MetadataLoadResult:

        db = SessionLocal()

        try:

            loader = MetadataLoader(db)

            result = MetadataLoadResult()

            tables = self.extract_tables()

            result.merge(
                loader.save_tables(tables)
            )

            columns = self.extract_columns()

            result.merge(
                loader.save_columns(columns)
            )

            relationships = (
                self.extract_relationships()
            )

            result.merge(
                loader.save_relationships(
                    relationships
                )
            )

            loader.create_log(result)

            return result

        finally:

            db.close()