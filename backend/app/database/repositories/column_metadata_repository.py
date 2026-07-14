from app.database.entities.column_metadata import ColumnMetadataEntity
from app.database.repositories.base_repository import BaseRepository
from datetime import datetime

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

    def update_profile(
        self,
        column_id: int,
        semantic_type: str | None,
        example_values: str | None,
        min_value,
        max_value,
        distinct_count: int,
    ) -> None:
        """
        Update semantic information of one column.
        """

        column = (
            self.db.query(ColumnMetadataEntity)
            .filter(
                ColumnMetadataEntity.id == column_id
            )
            .first()
        )

        if column is None:
            return

        column.semantic_type = semantic_type

        column.example_values = example_values

        column.min_value = (
            None
            if min_value is None
            else str(min_value)
        )

        column.max_value = (
            None
            if max_value is None
            else str(max_value)
        )

        column.distinct_count = distinct_count

        column.last_profiled = datetime.now()

        self.commit()