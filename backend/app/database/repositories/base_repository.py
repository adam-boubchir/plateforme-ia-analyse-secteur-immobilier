from typing import Any

from sqlalchemy.orm import Session


class BaseRepository:
    """
    Base repository providing common database operations.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def add(
        self,
        entity: Any,
    ) -> None:
        """
        Add a single entity to the current session.
        """

        self.db.add(entity)

    def add_all(
        self,
        entities: list[Any],
    ) -> None:
        """
        Add multiple entities to the current session.
        """

        self.db.add_all(entities)

    # =====================================================
    # TRANSACTION
    # =====================================================

    def flush(
        self,
    ) -> None:
        """
        Flush pending changes.
        """

        self.db.flush()

    def commit(
        self,
    ) -> None:
        """
        Commit current transaction.
        """

        self.db.commit()

    def rollback(
        self,
    ) -> None:
        """
        Roll back current transaction.
        """

        self.db.rollback()

    def refresh(
        self,
        entity: Any,
    ) -> None:
        """
        Refresh an entity from the database.
        """

        self.db.refresh(entity)

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        entity: Any,
    ) -> None:
        """
        Delete an entity.
        """

        self.db.delete(entity)