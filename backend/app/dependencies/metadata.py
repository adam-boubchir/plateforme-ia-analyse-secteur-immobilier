from sqlalchemy.orm import Session

from app.agents.sql_agent.context_engine.header_builder import (
    HeaderBuilder,
)
from app.agents.sql_agent.context_engine.table_context_builder import (
    TableContextBuilder,
)
from app.agents.sql_agent.context_engine.relationship_context_builder import (
    RelationshipContextBuilder,
)
from app.agents.sql_agent.context_engine.semantic_context_builder import (
    SemanticContextBuilder,
)
from app.agents.sql_agent.context_engine.business_rules_builder import (
    BusinessRulesBuilder,
)
from app.agents.sql_agent.context_engine.prompt_rules_builder import (
    PromptRulesBuilder,
)
from app.agents.sql_agent.context_engine.sql_context_builder import (
    SQLContextBuilder,
)

from app.agents.sql_agent.patterns.sql_pattern_builder import (
    SQLPatternBuilder,
)

from app.knowledge.business.business_knowledge_builder import (
    BusinessKnowledgeBuilder,
)
from app.knowledge.joins.join_knowledge_builder import (
    JoinKnowledgeBuilder,
)
from app.knowledge.joins.forbidden_join_builder import (
    ForbiddenJoinBuilder,
)

from app.database.repositories.table_metadata_repository import (
    TableMetadataRepository,
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

from app.services.metadata_service import (
    MetadataService,
)
from app.services.semantic_context_service import (
    SemanticContextService,
)

__all__ = [
    "get_metadata_service",
    "get_semantic_context_service",
    "get_sql_context_builder",
]


# ==========================================================
# METADATA SERVICE
# ==========================================================

def get_metadata_service(
    db: Session,
) -> MetadataService:

    table_repository = TableMetadataRepository(db)

    column_repository = ColumnMetadataRepository(db)

    relationship_repository = RelationshipRepository(db)

    return MetadataService(
        table_repository=table_repository,
        column_repository=column_repository,
        relationship_repository=relationship_repository,
    )


# ==========================================================
# SEMANTIC CONTEXT SERVICE
# ==========================================================

def get_semantic_context_service(
    db: Session,
) -> SemanticContextService:

    repository = SemanticContextRepository(db)

    return SemanticContextService(
        repository=repository,
    )


# ==========================================================
# SQL CONTEXT BUILDER
# ==========================================================

def get_sql_context_builder(
    db: Session,
) -> SQLContextBuilder:

    metadata_service = get_metadata_service(db)

    semantic_service = get_semantic_context_service(db)

    return SQLContextBuilder(
        header_builder=HeaderBuilder(),

        business_knowledge_builder=BusinessKnowledgeBuilder(),

        join_knowledge_builder=JoinKnowledgeBuilder(),

        forbidden_join_builder=ForbiddenJoinBuilder(),

        business_rules_builder=BusinessRulesBuilder(),

        sql_pattern_builder=SQLPatternBuilder(),

        table_builder=TableContextBuilder(
            metadata_service=metadata_service,
        ),

        relationship_builder=RelationshipContextBuilder(
            metadata_service=metadata_service,
        ),

        semantic_builder=SemanticContextBuilder(
            semantic_context_service=semantic_service,
        ),

        prompt_rules_builder=PromptRulesBuilder(),
    )