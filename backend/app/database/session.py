from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

# Import ORM entities so SQLAlchemy registers all mappings.
import app.database.entities_loader

from app.database.connection_immo_ai import (
    engine_immo_ai,
)
from app.database.connection_ministry import (
    engine_ministry,
)

__all__ = (
    "SessionLocalImmoAI",
    "SessionLocalMinistry",
    "get_immo_db",
    "get_ministry_db",
)


# ==========================================================
# SESSION FACTORIES
# ==========================================================

SessionLocalImmoAI: sessionmaker = sessionmaker(
    bind=engine_immo_ai,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

SessionLocalMinistry: sessionmaker = sessionmaker(
    bind=engine_ministry,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ==========================================================
# PRIVATE
# ==========================================================

def _get_session(
    *,
    factory: sessionmaker,
) -> Generator[Session, None, None]:
    """
    Create and safely dispose a SQLAlchemy session.

    Args:
        factory:
            SQLAlchemy session factory.

    Yields:
        An active SQLAlchemy session.

    Raises:
        Any database exception raised during session usage.
    """

    session = factory()

    try:
        yield session

    finally:
        session.close()


# ==========================================================
# PUBLIC
# ==========================================================

def get_immo_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session connected to the
    IMMO AI database.

    Yields:
        An active SQLAlchemy session.
    """

    yield from _get_session(
        factory=SessionLocalImmoAI,
    )


def get_ministry_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session connected to the
    Ministry SQL Server database.

    Yields:
        An active SQLAlchemy session.
    """

    yield from _get_session(
        factory=SessionLocalMinistry,
    )