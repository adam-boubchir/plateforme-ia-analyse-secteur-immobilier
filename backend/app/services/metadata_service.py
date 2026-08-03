from __future__ import annotations

from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)
from app.database.entities.relationship import (
    RelationshipEntity,
)
from app.database.entities.table_metadata import (
    TableMetadataEntity,
)
from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)
from app.database.repositories.relationship_repository import (
    RelationshipRepository,
)
from app.database.repositories.table_metadata_repository import (
    TableMetadataRepository,
)

__all__ = ("MetadataService",)


class MetadataService:
    """
    Provide database metadata required by the SQL Agent.

    This service acts as a thin abstraction layer over the metadata
    repositories and exposes a unified API for retrieving tables,
    columns and relationships.
    """

    def __init__(
        self,
        *,
        table_repository: TableMetadataRepository,
        column_repository: ColumnMetadataRepository,
        relationship_repository: RelationshipRepository,
    ) -> None:
        self._table_repository = table_repository
        self._column_repository = column_repository
        self._relationship_repository = relationship_repository

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get_tables(
        self,
    ) -> list[TableMetadataEntity]:
        """
        Retrieve every table available in the metadata catalog.

        Returns:
            List of table metadata.
        """

        tables = self._table_repository.get_all()

        return tables

    def get_table(
        self,
        *,
        schema_name: str,
        table_name: str,
    ) -> TableMetadataEntity | None:
        """
        Retrieve one table by its schema and name.

        Args:
            schema_name:
                Database schema.
            table_name:
                Table name.

        Returns:
            The matching table metadata, or None if not found.
        """

        table = self._table_repository.get_by_name(
            schema_name=schema_name,
            table_name=table_name,
        )

        return table

    def get_columns(
        self,
        *,
        table_name: str,
    ) -> list[ColumnMetadataEntity]:
        """
        Retrieve every column belonging to one table.

        Args:
            table_name:
                Table name.

        Returns:
            List of column metadata.
        """

        columns = self._column_repository.get_by_table(
            table_name=table_name,
        )

        return columns

    def get_relationships(
        self,
    ) -> list[RelationshipEntity]:
        """
        Retrieve every relationship between database tables.

        Returns:
            List of relationship metadata.
        """

        relationships = self._relationship_repository.get_all()

        return relationships