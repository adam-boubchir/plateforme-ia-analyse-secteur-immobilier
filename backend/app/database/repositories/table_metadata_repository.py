from app.database.entities.table_metadata import TableMetadataEntity
from app.database.repositories.base_repository import BaseRepository


class TableMetadataRepository(BaseRepository):
    """
    Repository for table metadata.
    """

    def create(
        self,
        table: TableMetadataEntity
    ) -> TableMetadataEntity:

        self.add(table)
        self.flush()

        return table

    def create_many(
        self,
        tables: list[TableMetadataEntity]
    ) -> None:

        self.add_all(tables)

    def get_by_name(
        self,
        schema_name: str,
        table_name: str
    ) -> TableMetadataEntity | None:

        return (
            self.db.query(TableMetadataEntity)
            .filter(
                TableMetadataEntity.schema_name == schema_name,
                TableMetadataEntity.table_name == table_name
            )
            .first()
        )

    def exists(
        self,
        schema_name: str,
        table_name: str
    ) -> bool:

        return (
            self.get_by_name(
                schema_name,
                table_name
            )
            is not None
        )

    def get_all(
        self
    ) -> list[TableMetadataEntity]:

        return (
            self.db.query(TableMetadataEntity)
            .order_by(
                TableMetadataEntity.schema_name,
                TableMetadataEntity.table_name
            )
            .all()
        )

    def delete_all(
        self
    ) -> None:

        self.db.query(
            TableMetadataEntity
        ).delete()