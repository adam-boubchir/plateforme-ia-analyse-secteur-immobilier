from sqlalchemy.orm import Session

from app.audit.audit_models import AuditReport

from app.database.repositories.table_metadata_repository import (
    TableMetadataRepository,
)

from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)

from app.database.repositories.relationship_repository import (
    RelationshipRepository,
)

from datetime import datetime, timezone

from app.database.entities.table_metadata import TableMetadataEntity

from app.database.entities.column_metadata import ColumnMetadataEntity

from app.database.entities.relationship import RelationshipEntity

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

__all__ = ["MetadataLoader"]

# ==========================================================
# CONSTANTS
# ==========================================================

FACT_TABLE_PREFIX = "FACT_"

FOREIGN_KEY_RELATIONSHIP = "FOREIGN KEY"

class MetadataLoader:
    """
    Load database metadata from an AuditReport
    into the IMMO_AI metadata database.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.table_repository = TableMetadataRepository(db)

        self.column_repository = ColumnMetadataRepository(db)

        self.relationship_repository = RelationshipRepository(db)
    
    def load(
        self,
        report: AuditReport,
    ) -> None:
        """
        Load all metadata into IMMO_AI.
        """
        
        logger.info("Starting metadata loading...")

        try:

            self._clear_metadata()

            self._load_tables(report)

            self._load_columns(report)

            self._load_relationships(report)

            self.db.commit()

            logger.info("Metadata loaded successfully.")

        except Exception:

            self.db.rollback()

            logger.exception("Metadata loading failed.")

            raise

    def _clear_metadata(self) -> None:
        """
        Remove all existing metadata before loading a new audit.
        """

        self.relationship_repository.delete_all()

        self.column_repository.delete_all()

        self.db.flush()

        self.table_repository.delete_all()

        self.db.flush()

    def _build_table_entity(
        self,
        report: AuditReport,
        table,
        row_count: int,
    ) -> TableMetadataEntity:
        """
        Build one table metadata entity.
        """

        return TableMetadataEntity(
            source_database=report.server.database_name,
            schema_name=table.schema_name,
            table_name=table.name,
            table_type=table.table_type,
            business_name=None,
            description=None,
            row_count=row_count,
            is_fact_table=table.name.upper().startswith(
                FACT_TABLE_PREFIX
            ),
            is_active=True,
            last_refresh=datetime.now(timezone.utc),
            updated_at=None,
        )

    def _load_tables(
        self,
        report: AuditReport,
    ) -> None:
        """
        Load all tables into table_metadata.
        """

        entities: list[TableMetadataEntity] = []

        row_counts: dict[tuple[str, str], int] = {

            (
                stat.schema_name,
                stat.table
            ): stat.row_count

            for stat in report.table_statistics

        }

        for table in report.tables:

            entities.append(
                self._build_table_entity(
                    report,
                    table,
                    row_counts.get(
                        (
                            table.schema_name,
                            table.name,
                        ),
                        0,
                    ),
                )
            )

        self.table_repository.create_many(entities)

        self.db.flush()

    def _build_column_entity(
        self,
        column,
        table_id: int,
        primary_keys: set[tuple[str, str, str]],
        foreign_keys: set[tuple[str, str, str]],
    ) -> ColumnMetadataEntity:
        """
        Build one column metadata entity.
        """

        return ColumnMetadataEntity(
            table_id=table_id,
            schema_name=column.schema_name,
            table_name=column.table,
            column_name=column.name,
            business_name=None,
            description=None,
            data_type=column.data_type,
            max_length=column.max_length,
            ordinal_position=None,
            default_value=column.default_value,
            is_nullable=column.nullable,
            is_primary_key=(
                (
                    column.schema_name,
                    column.table,
                    column.name,
                )
                in primary_keys
            ),
            is_foreign_key=(
                (
                    column.schema_name,
                    column.table,
                    column.name,
                )
                in foreign_keys
            ),
            sample_values=None,
            updated_at=None,
        )
        
    def _load_columns(
        self,
        report: AuditReport,
    ) -> None:
        """
        Load all columns into column_metadata.
        """
        entities: list[ColumnMetadataEntity] = []


        primary_keys: set[tuple[str, str, str]] = {
            (
                pk.schema_name,
                pk.table,
                pk.column
            )
            for pk in report.primary_keys
        }

        foreign_keys: set[tuple[str, str, str]] = {
            (
                fk.source_schema,
                fk.source_table,
                fk.source_column
            )
            for fk in report.foreign_keys
        }

        table_ids: dict[tuple[str, str], int] = {
            (
                table.schema_name,
                table.table_name
            ): table.id
            for table in self.table_repository.get_all()
        }

        for column in report.columns:

            table_id = table_ids.get(
                (
                    column.schema_name,
                    column.table,
                )
            )

            if table_id is None:
                continue

            entities.append(
                self._build_column_entity(
                    column=column,
                    table_id=table_id,
                    primary_keys=primary_keys,
                    foreign_keys=foreign_keys,
                )
            )

        self.column_repository.create_many(entities)

    def _build_relationship_entity(
        self,
        fk,
    ) -> RelationshipEntity:
        """
        Build one relationship metadata entity.
        """

        return RelationshipEntity(
            constraint_name=fk.constraint_name,
            source_schema=fk.source_schema,
            source_table=fk.source_table,
            source_column=fk.source_column,
            target_schema=fk.target_schema,
            target_table=fk.target_table,
            target_column=fk.target_column,
            relationship_type=FOREIGN_KEY_RELATIONSHIP,
            description=None,
            is_active=True,
            updated_at=None,
        )
        
    def _load_relationships(
        self,
        report: AuditReport,
    ) -> None:
        """
        Load all foreign key relationships into relationships.
        """

        entities: list[RelationshipEntity] = []

        for fk in report.foreign_keys:

            entities.append(
                self._build_relationship_entity(
                    fk,
                )
            )

        self.relationship_repository.create_many(entities)

                