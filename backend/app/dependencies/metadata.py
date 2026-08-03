from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.sql_agent.context_engine.business_rules_builder import (
    BusinessRulesBuilder,
)
from app.agents.sql_agent.context_engine.header_builder import (
    HeaderBuilder,
)
from app.agents.sql_agent.context_engine.prompt_rules_builder import (
    PromptRulesBuilder,
)
from app.agents.sql_agent.context_engine.relationship_context_builder import (
    RelationshipContextBuilder,
)
from app.agents.sql_agent.context_engine.semantic_context_builder import (
    SemanticContextBuilder,
)
from app.agents.sql_agent.context_engine.sql_context_builder import (
    SQLContextBuilder,
)
from app.agents.sql_agent.context_engine.table_context_builder import (
    TableContextBuilder,
)
from app.agents.sql_agent.patterns.sql_pattern_builder import (
    SQLPatternBuilder,
)
from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)
from app.database.repositories.relationship_repository import (
    RelationshipRepository,
)
from app.database.repositories.semantic_context_repository import (
    SemanticContextRepository,
)
from app.database.repositories.table_metadata_repository import (
    TableMetadataRepository,
)
from app.knowledge.business.business_knowledge_builder import (
    BusinessKnowledgeBuilder,
)
from app.knowledge.joins.forbidden_join_builder import (
    ForbiddenJoinBuilder,
)
from app.knowledge.joins.join_knowledge_builder import (
    JoinKnowledgeBuilder,
)
from app.services.metadata_service import (
    MetadataService,
)
from app.services.semantic_context_service import (
    SemanticContextService,
)

__all__ = (
    "get_metadata_service",
    "get_semantic_context_service",
    "get_sql_context_builder",
)


# ==========================================================
# METADATA SERVICE
# ==========================================================

def get_metadata_service(
    *,
    db: Session,
) -> MetadataService:
    """
    Build and return the MetadataService.

    Args:
        db: Application database session.

    Returns:
        A configured MetadataService.
    """

    table_repository = TableMetadataRepository(
        db=db,
    )

    column_repository = ColumnMetadataRepository(
        db=db,
    )

    relationship_repository = RelationshipRepository(
        db=db,
    )

    return MetadataService(
        table_repository=table_repository,
        column_repository=column_repository,
        relationship_repository=relationship_repository,
    )


# ==========================================================
# SEMANTIC CONTEXT SERVICE
# ==========================================================

def get_semantic_context_service(
    *,
    db: Session,
) -> SemanticContextService:
    """
    Build and return the SemanticContextService.

    Args:
        db: Application database session.

    Returns:
        A configured SemanticContextService.
    """

    repository = SemanticContextRepository(
        db=db,
    )

    return SemanticContextService(
        repository=repository,
    )


# ==========================================================
# SQL CONTEXT BUILDER
# ==========================================================

def get_sql_context_builder(
    *,
    db: Session,
) -> SQLContextBuilder:
    """
    Build and return the SQLContextBuilder.

    Args:
        db: Application database session.

    Returns:
        A fully configured SQLContextBuilder.
    """

    metadata_service = get_metadata_service(
        db=db,
    )

    semantic_service = get_semantic_context_service(
        db=db,
    )

    header_builder = HeaderBuilder()

    business_knowledge_builder = BusinessKnowledgeBuilder()

    join_knowledge_builder = JoinKnowledgeBuilder()

    forbidden_join_builder = ForbiddenJoinBuilder()

    business_rules_builder = BusinessRulesBuilder()

    sql_pattern_builder = SQLPatternBuilder()

    table_builder = TableContextBuilder(
        metadata_service=metadata_service,
    )

    relationship_builder = RelationshipContextBuilder(
        metadata_service=metadata_service,
    )

    semantic_builder = SemanticContextBuilder(
        semantic_context_service=semantic_service,
    )

    prompt_rules_builder = PromptRulesBuilder()

    return SQLContextBuilder(
        header_builder=header_builder,
        business_knowledge_builder=business_knowledge_builder,
        join_knowledge_builder=join_knowledge_builder,
        forbidden_join_builder=forbidden_join_builder,
        business_rules_builder=business_rules_builder,
        sql_pattern_builder=sql_pattern_builder,
        table_builder=table_builder,
        relationship_builder=relationship_builder,
        semantic_builder=semantic_builder,
        prompt_rules_builder=prompt_rules_builder,
    )