from __future__ import annotations

from app.services.metadata_service import (
    MetadataService,
)

from app.services.semantic_context_service import (
    SemanticContextService,
)

from .header_builder import (
    HeaderBuilder,
)

from .table_context_builder import (
    TableContextBuilder,
)

from .relationship_context_builder import (
    RelationshipContextBuilder,
)

from .semantic_context_builder import (
    SemanticContextBuilder,
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

from .business_rules_builder import (
    BusinessRulesBuilder,
)

from .prompt_rules_builder import (
    PromptRulesBuilder,
)

from typing import Any


class SQLContextBuilder:
    """
    Professional SQL Context Engine.

    Responsible for building every section of the
    SQL context sent to the LLM.
    """

    def __init__(
        self,
        header_builder: HeaderBuilder,
        business_knowledge_builder: BusinessKnowledgeBuilder,
        join_knowledge_builder: JoinKnowledgeBuilder,
        forbidden_join_builder: ForbiddenJoinBuilder,
        business_rules_builder: BusinessRulesBuilder,
        sql_pattern_builder: SQLPatternBuilder,
        table_builder: TableContextBuilder,
        relationship_builder: RelationshipContextBuilder,
        semantic_builder: SemanticContextBuilder,
        prompt_rules_builder: PromptRulesBuilder,
    ):

        self.header_builder = header_builder

        self.business_knowledge_builder = business_knowledge_builder

        self.join_knowledge_builder = join_knowledge_builder

        self.forbidden_join_builder = forbidden_join_builder

        self.business_rules_builder = business_rules_builder

        self.sql_pattern_builder = sql_pattern_builder

        self.table_builder = table_builder

        self.relationship_builder = relationship_builder

        self.semantic_builder = semantic_builder

        self.prompt_rules_builder = prompt_rules_builder
    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_context(
        self,
        question: str,
        selection: dict[str, Any],
    ) -> dict[str, str]:

        selected_tables = selection.get("tables", [])

        sections = self._build_sections(
            question,
            selection,
            selected_tables,
        )

        full_context = self._build_full_context(
            sections,
        )

        return self._build_result(
            sections,
            full_context,
        )

    def _build_sections(
        self,
        question: str,
        selection: dict[str, Any],
        selected_tables: list[str],
    ) -> dict[str, list[str]]:

        return {
            "header": self.header_builder.build(),
            "business": self.business_knowledge_builder.build(selected_tables),
            "joins": self.join_knowledge_builder.build(selected_tables),
            "forbidden": self.forbidden_join_builder.build(selected_tables),
            "business_rules": self.business_rules_builder.build(),
            "sql_patterns": self.sql_pattern_builder.build(
                question=question,
                selection=selection,
            ),
            "tables": self.table_builder.build(selected_tables),
            "relationships": self.relationship_builder.build(selected_tables),
            "semantic": self.semantic_builder.build(question),
            "prompt_rules": self.prompt_rules_builder.build(),
        }

    def _build_full_context(
        self,
        sections: dict,
    ) -> str:

        context = []

        for value in sections.values():
            context.extend(value)

        return "\n".join(context)

    def _build_result(
        self,
        sections: dict,
        full_context: str,
    ) -> dict:

        return {
            "business_knowledge": "\n".join(sections["business"]),
            "join_knowledge": "\n".join(sections["joins"]),
            "forbidden_joins": "\n".join(sections["forbidden"]),
            "semantic_context": "\n".join(sections["semantic"]),
            "sql_patterns": "\n".join(sections["sql_patterns"]),
            "full_context": full_context,
        }