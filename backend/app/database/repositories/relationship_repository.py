from app.database.entities.relationship import RelationshipEntity
from app.database.repositories.base_repository import BaseRepository


class RelationshipRepository(BaseRepository):
    """
    Repository for relationships.
    """

    def create(
        self,
        relationship: RelationshipEntity
    ) -> RelationshipEntity:

        self.add(relationship)
        self.flush()

        return relationship

    def create_many(
        self,
        relationships: list[RelationshipEntity]
    ) -> None:

        self.add_all(relationships)

    def get_all(
        self
    ) -> list[RelationshipEntity]:

        return (
            self.db.query(RelationshipEntity)
            .order_by(
                RelationshipEntity.source_table,
                RelationshipEntity.target_table
            )
            .all()
        )

    def delete_all(
        self
    ) -> None:

        self.db.query(
            RelationshipEntity
        ).delete()