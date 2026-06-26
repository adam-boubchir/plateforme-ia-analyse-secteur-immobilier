from sqlalchemy import select
from sqlalchemy.orm import Session

from app.metadata.metadata_models import (
    TableMetadata,
    ColumnMetadata,
    MetadataLoadResult,
    RelationshipMetadata
)

from app.database.entities.table_metadata import (
    TableMetadataEntity
)

from app.database.entities.column_metadata import (
    ColumnMetadataEntity
)

from app.database.entities.relationship import (
    RelationshipEntity
)

import uuid

from app.database.entities.agent_log import (
    AgentLogEntity
)

from app.metadata.constants import (
    METADATA_AGENT_NAME,
    STATUS_SUCCESS,
    STATUS_ERROR
)

class MetadataLoader:

    def __init__(self, db: Session):
        self.db = db

    def _build_table_key(
        self,
        source_database: str,
        schema_name_name: str,
        table_name: str
    ) -> tuple:

        return (
            source_database,
            schema_name_name,
            table_name
        )

    def _build_column_key(
        self,
        table_name: str,
        column_name: str
    ) -> tuple:

        return (
            table_name,
            column_name
        )
    def save_tables(
        self,
        tables: list[TableMetadata]
    ) -> MetadataLoadResult:

        result = MetadataLoadResult()

        try:

            existing_tables = self.db.scalars(
                select(TableMetadataEntity)
            ).all()

            existing_tables_dict = {
                self._build_table_key(
                    table.source_database,
                    table.schema_name_name,
                    table.table_name
                ): table
                for table in existing_tables
            }

            for table in tables:

                try:

                    table_key = self._build_table_key(
                        table.source_database,
                        table.schema_name_name,
                        table.table_name
                    )

                    existing_table = existing_tables_dict.get(
                        table_key
                    )

                    if existing_table:

                        existing_table.business_name = (
                            table.business_name
                        )

                        existing_table.description = (
                            table.description
                        )

                        existing_table.row_count = (
                            table.row_count
                        )

                        existing_table.is_active = (
                            table.is_active
                        )

                    else:

                        new_table = TableMetadataEntity(
                            source_database=table.source_database,
                            schema_name_name=table.schema_name_name,
                            table_name=table.table_name,
                            business_name=table.business_name,
                            description=table.description,
                            row_count=table.row_count,
                            is_active=table.is_active
                        )

                        self.db.add(new_table)

                    result.tables_processed += 1

                except Exception as e:

                    result.errors.append(
                        f"Table {table.table_name}: {str(e)}"
                    )

                    result.success = False

            self.db.commit()

        except Exception as e:

            self.db.rollback()

            result.errors.append(str(e))

            result.success = False

        return result
    
    def _add_error(
        self,
        result: MetadataLoadResult,
        message: str
    ) -> None:

        result.errors.append(message)
        result.success = False
    
    def save_columns(
        self,
        columns: list[ColumnMetadata]
    ) -> MetadataLoadResult:

        result = MetadataLoadResult()

        try:

            # Chargement des tables déjà enregistrées
            tables = self.db.scalars(
                select(TableMetadataEntity)
            ).all()

            table_mapping = {
                table.table_name: table.id
                for table in tables
            }

            existing_columns = self.db.scalars(
                select(ColumnMetadataEntity)
            ).all()

            existing_columns_dict = {
                self._build_column_key(
                    column.table_name,
                    column.column_name
                ): column
                for column in existing_columns
            }

            for column in columns:

                try:

                    table_id = table_mapping.get(
                        column.table_name
                    )

                    if table_id is None:

                        result.warnings.append(
                            f"Table not found for column "
                            f"{column.table_name}"
                        )

                        continue

                    column_key = self._build_column_key(
                        column.table_name,
                        column.column_name
                    )

                    existing_column = (
                        existing_columns_dict.get(
                            column_key
                        )
                    )

                    if existing_column:

                        existing_column.business_name = (
                            column.business_name
                        )

                        existing_column.description = (
                            column.description
                        )

                        existing_column.data_type = (
                            column.data_type
                        )

                        existing_column.is_nullable = (
                            column.is_nullable
                        )

                        existing_column.is_primary_key = (
                            column.is_primary_key
                        )

                        existing_column.is_foreign_key = (
                            column.is_foreign_key
                        )

                        existing_column.sample_values = (
                            column.sample_values
                        )

                    else:

                        new_column = ColumnMetadataEntity(
                            table_id=table_id,
                            table_name=column.table_name,
                            column_name=column.column_name,
                            business_name=column.business_name,
                            description=column.description,
                            data_type=column.data_type,
                            is_nullable=column.is_nullable,
                            is_primary_key=column.is_primary_key,
                            is_foreign_key=column.is_foreign_key,
                            sample_values=column.sample_values
                        )

                        self.db.add(new_column)

                    result.columns_processed += 1

                except Exception as e:

                    self._add_error(
                        result,
                        f"Column {column.column_name}: {str(e)}"
                    )

            if result.columns_processed > 0:
                self.db.commit()

        except Exception as e:

            self.db.rollback()

            self._add_error(
                result,
                str(e)
            )

        return result
    
    
    def _build_relationship_key(
        self,
        source_table: str,
        source_column: str,
        target_table: str,
        target_column: str
    ) -> tuple:

        return (
            source_table,
            source_column,
            target_table,
            target_column
        )
    
    def save_relationships(
        self,
        relationships: list[RelationshipMetadata]
    ) -> MetadataLoadResult:

        result = MetadataLoadResult()

        try:

            existing_relationships = self.db.scalars(
                select(RelationshipEntity)
            ).all()

            existing_relationships_dict = {
                self._build_relationship_key(
                    relation.source_table,
                    relation.source_column,
                    relation.target_table,
                    relation.target_column
                ): relation
                for relation in existing_relationships
            }

            for relationship in relationships:

                try:

                    relationship_key = (
                        self._build_relationship_key(
                            relationship.source_table,
                            relationship.source_column,
                            relationship.target_table,
                            relationship.target_column
                        )
                    )

                    existing_relationship = (
                        existing_relationships_dict.get(
                            relationship_key
                        )
                    )

                    if existing_relationship:

                        existing_relationship.relationship_type = (
                            relationship.relationship_type
                        )

                        existing_relationship.description = (
                            relationship.description
                        )

                    else:

                        new_relationship = RelationshipEntity(
                            source_table=relationship.source_table,
                            source_column=relationship.source_column,
                            target_table=relationship.target_table,
                            target_column=relationship.target_column,
                            relationship_type=relationship.relationship_type,
                            description=relationship.description
                        )

                        self.db.add(new_relationship)

                    result.relationships_processed += 1

                except Exception as e:

                    self._add_error(
                        result,
                        f"Relationship error: {str(e)}"
                    )

            if result.relationships_processed > 0:
                self.db.commit()

        except Exception as e:

            self.db.rollback()

            self._add_error(
                result,
                str(e)
            )

        return result
    
    def _build_log_message(
        self,
        result: MetadataLoadResult
    ) -> str:

        return (
            f"Tables={result.tables_processed}, "
            f"Columns={result.columns_processed}, "
            f"Relationships={result.relationships_processed}, "
            f"Errors={len(result.errors)}"
        )
    
    def create_log(
        self,
        result: MetadataLoadResult
    ) -> None:

        try:

            log = AgentLogEntity(

                request_id=str(uuid.uuid4()),

                agent_name=METADATA_AGENT_NAME,

                status=(
                    STATUS_SUCCESS
                    if result.success
                    else STATUS_ERROR
                ),

                user_question=None,

                generated_sql=None,

                model_name=None,

                user_id=None,

                execution_time_ms=None,

                rows_returned=None,

                error_message=(
                    "\n".join(result.errors)
                    if result.errors
                    else None
                )
            )

            self.db.add(log)

            self.db.commit()

        except Exception as e:

            self.db.rollback()

            print(
                f"Error while creating log: {e}"
            )
    
    def load(
        self,
        tables: list[TableMetadata],
        columns: list[ColumnMetadata],
        relationships: list[RelationshipMetadata]
    ) -> MetadataLoadResult:

        result = MetadataLoadResult()

        result.merge(
            self.save_tables(tables)
        )

        result.merge(
            self.save_columns(columns)
        )

        result.merge(
            self.save_relationships(
                relationships
            )
        )

        self.create_log(result)

        return result