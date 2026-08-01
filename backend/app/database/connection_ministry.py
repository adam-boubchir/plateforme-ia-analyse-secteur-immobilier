from sqlalchemy import Engine, create_engine

from app.database.config import settings


# ==========================================================
# CONNECTION STRING
# ==========================================================

ODBC_DRIVER = "ODBC Driver 17 for SQL Server"

CONNECTION_STRING = (
    f"mssql+pyodbc://"
    f"{settings.SQL_USERNAME}:{settings.SQL_PASSWORD}"
    f"@{settings.MINISTRY_SERVER}"
    f"/{settings.MINISTRY_DATABASE}"
    f"?driver={ODBC_DRIVER.replace(' ', '+')}"
)


# ==========================================================
# SQLALCHEMY ENGINE
# ==========================================================

engine_ministry: Engine = create_engine(
    CONNECTION_STRING,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=30,
    echo=False,
    future=True,
)


__all__ = [
    "engine_ministry",
]