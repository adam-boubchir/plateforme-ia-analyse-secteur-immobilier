from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.orm import Session

from app.database.entities.table_metadata import (
    TableMetadataEntity,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class TableMetadataRepository(BaseRepository):
    """
    Repository responsible for table metadata persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(db=db)

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        table: TableMetadataEntity,
    ) -> TableMetadataEntity:
        """
        Persist a table metadata entry.
        """

        self.add(
            entity=table,
        )

        self.flush()

        return table

    def create_many(
        self,
        tables: list[TableMetadataEntity],
    ) -> None:
        """
        Persist multiple table metadata entries.
        """

        self.add_all(
            entities=tables,
        )

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_name(
        self,
        schema_name: str,
        table_name: str,
    ) -> TableMetadataEntity | None:
        """
        Retrieve one table by schema and table name.
        """

        statement = (
            select(
                TableMetadataEntity,
            )
            .where(
                TableMetadataEntity.schema_name == schema_name,
                TableMetadataEntity.table_name == table_name,
            )
        )

        return self.db.scalar(
            statement,
        )

    def exists(
        self,
        schema_name: str,
        table_name: str,
    ) -> bool:
        """
        Check whether a table metadata entry exists.
        """

        return (
            self.get_by_name(
                schema_name=schema_name,
                table_name=table_name,
            )
            is not None
        )

    def get_all(
        self,
    ) -> list[TableMetadataEntity]:
        """
        Retrieve every table metadata entry.
        """

        statement = (
            select(
                TableMetadataEntity,
            )
            .order_by(
                TableMetadataEntity.schema_name,
                TableMetadataEntity.table_name,
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_all(
        self,
    ) -> None:
        """
        Delete every table metadata entry.
        """

        statement = delete(
            TableMetadataEntity,
        )

        self.db.execute(
            statement,
        )


__all__ = [
    "TableMetadataRepository",
]