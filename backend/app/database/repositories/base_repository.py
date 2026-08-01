from typing import Any

from sqlalchemy.orm import Session


class BaseRepository:
    """
    Base repository providing common database operations.

    Responsibilities
    ----------------
    • Add entities
    • Delete entities
    • Manage transactions
    • Refresh ORM entities
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db: Session = db

    # =====================================================
    # CREATE
    # =====================================================

    def add(
        self,
        entity: Any,
    ) -> None:
        """
        Add one entity to the current session.
        """

        self.db.add(
            instance=entity,
        )

    def add_all(
        self,
        entities: list[Any],
    ) -> None:
        """
        Add multiple entities to the current session.
        """

        self.db.add_all(
            instances=entities,
        )

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
        Commit the current transaction.
        """

        self.db.commit()

    def rollback(
        self,
    ) -> None:
        """
        Roll back the current transaction.
        """

        self.db.rollback()

    def refresh(
        self,
        entity: Any,
    ) -> None:
        """
        Refresh an ORM entity.
        """

        self.db.refresh(
            instance=entity,
        )

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

        self.db.delete(
            instance=entity,
        )


__all__ = [
    "BaseRepository",
]