from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.orm import Session

from app.database.entities.relationship import (
    RelationshipEntity,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class RelationshipRepository(BaseRepository):
    """
    Repository responsible for relationship metadata persistence.
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
        relationship: RelationshipEntity,
    ) -> RelationshipEntity:
        """
        Persist one relationship.
        """

        self.add(
            entity=relationship,
        )

        self.flush()

        return relationship

    def create_many(
        self,
        relationships: list[RelationshipEntity],
    ) -> None:
        """
        Persist multiple relationships.
        """

        self.add_all(
            entities=relationships,
        )

    # ==========================================================
    # READ
    # ==========================================================

    def get_all(
        self,
    ) -> list[RelationshipEntity]:
        """
        Retrieve every relationship ordered by source and target tables.
        """

        statement = (
            select(
                RelationshipEntity,
            )
            .order_by(
                RelationshipEntity.source_table,
                RelationshipEntity.target_table,
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
        Delete every relationship.
        """

        statement = delete(
            RelationshipEntity,
        )

        self.db.execute(
            statement,
        )


__all__ = [
    "RelationshipRepository",
]