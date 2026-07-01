from sqlalchemy.orm import Session

from app.services.metadata_service import (
    MetadataService,
)

from app.agents.sql_agent.sql_context_builder import (
    SQLContextBuilder,
)


def get_metadata_service(
    db: Session,
) -> MetadataService:
    """
    Dependency returning the MetadataService.
    """

    return MetadataService(db)


def get_sql_context_builder(
    db: Session,
) -> SQLContextBuilder:
    """
    Dependency returning the SQLContextBuilder.
    """

    metadata_service = get_metadata_service(db)

    return SQLContextBuilder(
        metadata_service
    )