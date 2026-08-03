from __future__ import annotations

from urllib.parse import quote_plus

from sqlalchemy import (
    Engine,
    create_engine,
)

from app.database.config import (
    settings,
)

__all__ = (
    "engine_immo_ai",
)


# ==========================================================
# CONSTANTS
# ==========================================================

_SQL_SERVER_ODBC_DRIVER = "ODBC Driver 17 for SQL Server"


# ==========================================================
# PRIVATE
# ==========================================================

def _build_connection_string() -> str:
    """
    Build the SQLAlchemy connection string for the
    IMMO AI database.

    Returns:
        A SQLAlchemy connection string.
    """

    driver = quote_plus(
        _SQL_SERVER_ODBC_DRIVER,
    )

    return (
        "mssql+pyodbc://"
        f"{settings.SQL_USERNAME}:{settings.SQL_PASSWORD}"
        f"@{settings.IMMO_AI_SERVER}"
        f"/{settings.IMMO_AI_DATABASE}"
        f"?driver={driver}"
    )


# ==========================================================
# ENGINE
# ==========================================================

_IMMO_AI_CONNECTION_STRING = _build_connection_string()

engine_immo_ai: Engine = create_engine(
    _IMMO_AI_CONNECTION_STRING,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=30,
    pool_size=10,
    max_overflow=20,
    echo=False,
    future=True,
)