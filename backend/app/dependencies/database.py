from sqlalchemy.orm import Session

from app.database.session import (
    get_immo_db,
    get_ministry_db,
)


def get_immo_session() -> Session:
    """
    Dependency returning the IMMO_AI database session.
    """

    return next(get_immo_db())


def get_ministry_session() -> Session:
    """
    Dependency returning the Ministry database session.
    """

    return next(get_ministry_db())