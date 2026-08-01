from datetime import datetime

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.orm import Session

from app.database.entities.column_metadata import (
    ColumnMetadataEntity,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class ColumnMetadataRepository(BaseRepository):
    """
    Repository responsible for column metadata persistence.
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
        column: ColumnMetadataEntity,
    ) -> ColumnMetadataEntity:
        """
        Persist a column metadata entry.
        """

        self.add(
            entity=column,
        )

        self.flush()

        return column

    def create_many(
        self,
        columns: list[ColumnMetadataEntity],
    ) -> None:
        """
        Persist multiple column metadata entries.
        """

        self.add_all(
            entities=columns,
        )

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_name(
        self,
        table_name: str,
        column_name: str,
    ) -> ColumnMetadataEntity | None:
        """
        Retrieve one column by table and column name.
        """

        statement = (
            select(
                ColumnMetadataEntity,
            )
            .where(
                ColumnMetadataEntity.table_name == table_name,
                ColumnMetadataEntity.column_name == column_name,
            )
        )

        return self.db.scalar(
            statement,
        )

    def get_by_table(
        self,
        table_name: str,
    ) -> list[ColumnMetadataEntity]:
        """
        Retrieve every column of one table.
        """

        statement = (
            select(
                ColumnMetadataEntity,
            )
            .where(
                ColumnMetadataEntity.table_name == table_name,
            )
            .order_by(
                ColumnMetadataEntity.ordinal_position,
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
        Delete every column metadata entry.
        """

        statement = delete(
            ColumnMetadataEntity,
        )

        self.db.execute(
            statement,
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_profile(
        self,
        column_id: int,
        semantic_type: str | None,
        example_values: str | None,
        min_value: object | None,
        max_value: object | None,
        distinct_count: int,
    ) -> None:
        """
        Update semantic information of one column.
        """

        statement = (
            select(
                ColumnMetadataEntity,
            )
            .where(
                ColumnMetadataEntity.id == column_id,
            )
        )

        column = self.db.scalar(
            statement,
        )

        if column is None:
            return

        column.semantic_type = semantic_type
        column.example_values = example_values
        column.min_value = (
            None if min_value is None else str(min_value)
        )
        column.max_value = (
            None if max_value is None else str(max_value)
        )
        column.distinct_count = distinct_count
        column.last_profiled = datetime.now()

        self.commit()


__all__ = [
    "ColumnMetadataRepository",
]