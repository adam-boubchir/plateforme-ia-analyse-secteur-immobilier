from collections.abc import Generator

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

import app.database.entities_loader

from app.database.connection_immo_ai import (
    engine_immo_ai,
)
from app.database.connection_ministry import (
    engine_ministry,
)


# ==========================================================
# SESSION FACTORIES
# ==========================================================

SessionLocalImmoAI = sessionmaker(
    bind=engine_immo_ai,
    autocommit=False,
    autoflush=False,
)

SessionLocalMinistry = sessionmaker(
    bind=engine_ministry,
    autocommit=False,
    autoflush=False,
)


# ==========================================================
# IMMO AI DATABASE
# ==========================================================

def get_immo_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session for the IMMO AI database.
    """

    db: Session = SessionLocalImmoAI()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# MINISTRY DATABASE
# ==========================================================

def get_ministry_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session for the Ministry database.
    """

    db: Session = SessionLocalMinistry()

    try:
        yield db

    finally:
        db.close()


__all__ = [
    "SessionLocalImmoAI",
    "SessionLocalMinistry",
    "get_immo_db",
    "get_ministry_db",
]