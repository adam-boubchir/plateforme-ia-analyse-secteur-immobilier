from typing import Any

from sqlalchemy.orm import Session


class BaseRepository:
    """
    Base class for all repositories.
    """

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def add(
        self,
        entity: Any
    ) -> None:
        """
        Add one entity to the current session.
        """
        self.db.add(entity)

    def add_all(
        self,
        entities: list[Any]
    ) -> None:
        """
        Add multiple entities to the current session.
        """
        self.db.add_all(entities)

    def flush(self) -> None:
        """
        Flush pending changes.
        """
        self.db.flush()

    def commit(self) -> None:
        """
        Commit current transaction.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """
        self.db.rollback()