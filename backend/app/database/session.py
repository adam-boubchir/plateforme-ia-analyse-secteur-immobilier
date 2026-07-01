from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.connection_immo_ai import engine_immo_ai
from app.database.connection_ministry import engine_ministry
import app.database.entities_loader


SessionLocalImmoAI = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_immo_ai
)

SessionLocalMinistry = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_ministry
)


def get_immo_db() -> Session:

    db = SessionLocalImmoAI()

    try:
        yield db

    finally:
        db.close()


def get_ministry_db() -> Session:

    db = SessionLocalMinistry()

    try:
        yield db

    finally:
        db.close()