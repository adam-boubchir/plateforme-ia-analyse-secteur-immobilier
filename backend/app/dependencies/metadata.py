from sqlalchemy.orm import Session

from app.services.metadata_service import (
    MetadataService,
)

from app.services.semantic_context_service import (
    SemanticContextService,
)

from app.database.repositories.semantic_context_repository import (
    SemanticContextRepository,
)

from app.agents.sql_agent.context_engine.sql_context_builder import (
    SQLContextBuilder,
)


def get_metadata_service(
    db: Session,
) -> MetadataService:
    """
    Dependency returning the MetadataService.
    """

    return MetadataService(db)


def get_semantic_context_service(
    db: Session,
) -> SemanticContextService:
    """
    Dependency returning the SemanticContextService.
    """

    repository = SemanticContextRepository(
        db
    )

    return SemanticContextService(
        repository
    )


def get_sql_context_builder(
    db: Session,
) -> SQLContextBuilder:
    """
    Dependency returning the professional SQLContextBuilder.
    """

    metadata_service = get_metadata_service(
        db
    )

    semantic_context_service = (
        get_semantic_context_service(
            db
        )
    )

    return SQLContextBuilder(
        metadata_service=metadata_service,
        semantic_context_service=semantic_context_service,
    )