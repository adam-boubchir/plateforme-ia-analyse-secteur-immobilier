from app.database.entities.column_metadata import ColumnMetadataEntity
from app.database.repositories.base_repository import BaseRepository


class ColumnMetadataRepository(BaseRepository):
    """
    Repository for column metadata.
    """

    def create(
        self,
        column: ColumnMetadataEntity
    ) -> ColumnMetadataEntity:

        self.add(column)
        self.flush()

        return column

    def create_many(
        self,
        columns: list[ColumnMetadataEntity]
    ) -> None:

        self.add_all(columns)

    def get_by_name(
        self,
        table_name: str,
        column_name: str
    ) -> ColumnMetadataEntity | None:

        return (
            self.db.query(ColumnMetadataEntity)
            .filter(
                ColumnMetadataEntity.table_name == table_name,
                ColumnMetadataEntity.column_name == column_name
            )
            .first()
        )

    def get_by_table(
        self,
        table_name: str
    ) -> list[ColumnMetadataEntity]:

        return (
            self.db.query(ColumnMetadataEntity)
            .filter(
                ColumnMetadataEntity.table_name == table_name
            )
            .order_by(
                ColumnMetadataEntity.ordinal_position
            )
            .all()
        )

    def delete_all(
        self
    ) -> None:

        self.db.query(
            ColumnMetadataEntity
        ).delete()