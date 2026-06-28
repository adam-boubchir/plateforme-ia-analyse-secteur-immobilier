from sqlalchemy.orm import Session

from app.database.repositories.table_metadata_repository import (
    TableMetadataRepository,
)

from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)

from app.database.repositories.relationship_repository import (
    RelationshipRepository,
)


class MetadataService:
    """
    Service responsible for providing database metadata
    to the SQL Agent.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.table_repository = TableMetadataRepository(db)

        self.column_repository = ColumnMetadataRepository(db)

        self.relationship_repository = RelationshipRepository(db)

    def get_tables(
        self,
    ):
        """
        Return all database tables.
        """

        return self.table_repository.get_all()
    
    def get_table(
        self,
        schema_name: str,
        table_name: str,
    ):
        """
        Return one table.
        """

        return self.table_repository.get_by_name(
            schema_name,
            table_name,
        )
    
    def get_columns(
        self,
        table_name: str,
    ):
        """
        Return all columns of one table.
        """

        return self.column_repository.get_by_table(
            table_name
        )
    
    def get_relationships(
        self,
    ):
        """
        Return all relationships.
        """

        return self.relationship_repository.get_all()