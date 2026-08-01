from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import (
    get_immo_db,
    get_ministry_db,
)


def get_immo_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency providing an IMMO_AI database session.
    """
    yield from get_immo_db()


def get_ministry_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency providing a Ministry database session.
    """
    yield from get_ministry_db()