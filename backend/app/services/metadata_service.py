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


class MetadataService:
    """
    Service responsible for providing database metadata
    to the SQL Agent.
    """

    def __init__(
        self,
        table_repository: TableMetadataRepository,
        column_repository: ColumnMetadataRepository,
        relationship_repository: RelationshipRepository,
    ) -> None:

        self.table_repository: TableMetadataEntityRepository = (
            table_repository
        )

        self.column_repository: ColumnMetadataRepository = (
            column_repository
        )

        self.relationship_repository: RelationshipRepository = (
            relationship_repository
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get_tables(
        self,
    ) -> list[TableMetadataEntity]:
        """
        Return all database tables.
        """

        return self.table_repository.get_all()

    def get_table(
        self,
        schema_name: str,
        table_name: str,
    ) -> TableMetadataEntity | None:
        """
        Return one table.
        """

        return self.table_repository.get_by_name(
            schema_name=schema_name,
            table_name=table_name,
        )

    def get_columns(
        self,
        table_name: str,
    ) -> list[ColumnMetadataEntity]:
        """
        Return all columns of one table.
        """

        return self.column_repository.get_by_table(
            table_name=table_name,
        )

    def get_relationships(
        self,
    ) -> list[RelationshipEntity]:
        """
        Return all relationships.
        """

        return self.relationship_repository.get_all()


__all__ = [
    "MetadataService",
]