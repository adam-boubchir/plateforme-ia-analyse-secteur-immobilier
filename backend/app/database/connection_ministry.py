from sqlalchemy import create_engine

from app.database.config import settings


connection_string = (
    f"mssql+pyodbc://{settings.SQL_USERNAME}:{settings.SQL_PASSWORD}"
    f"@{settings.MINISTRY_SERVER}/{settings.MINISTRY_DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine_ministry = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)