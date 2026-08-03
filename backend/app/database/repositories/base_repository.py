from __future__ import annotations

from typing import TypeVar

from sqlalchemy.orm import Session

__all__ = (
    "BaseRepository",
)

T = TypeVar("T")


class BaseRepository:
    """
    Base repository providing common database operations.

    Responsibilities
    ----------------
    - Add entities.
    - Delete entities.
    - Manage transactions.
    - Refresh ORM entities.
    """

    def __init__(
        self,
        *,
        db: Session,
    ) -> None:
        self._db = db

    # =====================================================
    # CREATE
    # =====================================================

    def add(
        self,
        *,
        entity: T,
    ) -> T:
        """
        Add one entity to the current session.

        Args:
            entity:
                ORM entity to add.

        Returns:
            The persisted entity.
        """

        self._db.add(
            entity,
        )

        return entity

    def add_all(
        self,
        *,
        entities: list[T],
    ) -> list[T]:
        """
        Add multiple entities to the current session.

        Args:
            entities:
                ORM entities to add.

        Returns:
            The persisted entities.
        """

        self._db.add_all(
            entities,
        )

        return entities

    def merge(
        self,
        *,
        entity: T,
    ) -> T:
        """
        Merge an entity into the current session.

        Args:
            entity:
                ORM entity.

        Returns:
            The managed entity.
        """

        merged_entity = self._db.merge(
            entity,
        )

        return merged_entity

    # =====================================================
    # TRANSACTION
    # =====================================================

    def flush(
        self,
    ) -> None:
        """
        Flush pending changes.
        """

        self._db.flush()

    def commit(
        self,
    ) -> None:
        """
        Commit the current transaction.
        """

        self._db.commit()

    def rollback(
        self,
    ) -> None:
        """
        Roll back the current transaction.
        """

        self._db.rollback()

    def refresh(
        self,
        *,
        entity: T,
    ) -> None:
        """
        Refresh an ORM entity.

        Args:
            entity:
                ORM entity to refresh.
        """

        self._db.refresh(
            entity,
        )

    def close(
        self,
    ) -> None:
        """
        Close the current session.
        """

        self._db.close()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        *,
        entity: T,
    ) -> None:
        """
        Delete an entity.

        Args:
            entity:
                ORM entity to delete.
        """

        self._db.delete(
            entity,
        )