from __future__ import annotations

from typing import Any

from app.agents.sql_agent.patterns.sql_pattern_builder import (
    SQLPatternBuilder,
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

from .business_rules_builder import BusinessRulesBuilder
from .header_builder import HeaderBuilder
from .prompt_rules_builder import PromptRulesBuilder
from .relationship_context_builder import RelationshipContextBuilder
from .semantic_context_builder import SemanticContextBuilder
from .table_context_builder import TableContextBuilder

__all__ = ("SQLContextBuilder",)


class SQLContextBuilder:
    """
    Build the complete context sent to the SQL language model.

    Responsibilities
    ----------------
    - Build every context section.
    - Assemble the complete prompt context.
    - Return both the individual sections and the full context.
    """

    def __init__(
        self,
        *,
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
    ) -> None:
        self._header_builder = header_builder
        self._business_knowledge_builder = business_knowledge_builder
        self._join_knowledge_builder = join_knowledge_builder
        self._forbidden_join_builder = forbidden_join_builder
        self._business_rules_builder = business_rules_builder
        self._sql_pattern_builder = sql_pattern_builder
        self._table_builder = table_builder
        self._relationship_builder = relationship_builder
        self._semantic_builder = semantic_builder
        self._prompt_rules_builder = prompt_rules_builder

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_context(
        self,
        *,
        question: str,
        selection: dict[str, Any],
    ) -> dict[str, str]:
        """
        Build the complete SQL context.

        Args:
            question:
                User natural-language question.

            selection:
                Knowledge selected for this question.

        Returns:
            Dictionary containing every context section together with the
            complete prompt context.
        """

        selected_tables = selection.get(
            "tables",
            [],
        )

        sections = self._build_sections(
            question=question,
            selection=selection,
            selected_tables=selected_tables,
        )

        full_context = self._build_full_context(
            sections=sections,
        )

        context = self._build_result(
            sections=sections,
            full_context=full_context,
        )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_sections(
        self,
        *,
        question: str,
        selection: dict[str, Any],
        selected_tables: list[str],
    ) -> dict[str, list[str]]:
        """
        Build every context section independently.
        """

        sections = {
            "header": self._header_builder.build(),
            "business": self._business_knowledge_builder.build(
                selected_tables=selected_tables,
            ),
            "joins": self._join_knowledge_builder.build(
                selected_tables=selected_tables,
            ),
            "forbidden": self._forbidden_join_builder.build(
                selected_tables=selected_tables,
            ),
            "business_rules": self._business_rules_builder.build(),
            "sql_patterns": self._sql_pattern_builder.build(
                question=question,
                selection=selection,
            ),
            "tables": self._table_builder.build(
                selected_tables=selected_tables,
            ),
            "relationships": self._relationship_builder.build(
                selected_tables=selected_tables,
            ),
            "semantic": self._semantic_builder.build(
                question=question,
            ),
            "prompt_rules": self._prompt_rules_builder.build(),
        }

        return sections

    @staticmethod
    def _build_full_context(
        *,
        sections: dict[str, list[str]],
    ) -> str:
        """
        Concatenate every context section.
        """

        full_context = "\n".join(
            line
            for section in sections.values()
            for line in section
        )

        return full_context

    @staticmethod
    def _build_result(
        *,
        sections: dict[str, list[str]],
        full_context: str,
    ) -> dict[str, str]:
        """
        Build the final context payload.
        """

        context = {
            "business_knowledge": "\n".join(
                sections["business"],
            ),
            "join_knowledge": "\n".join(
                sections["joins"],
            ),
            "forbidden_joins": "\n".join(
                sections["forbidden"],
            ),
            "semantic_context": "\n".join(
                sections["semantic"],
            ),
            "sql_patterns": "\n".join(
                sections["sql_patterns"],
            ),
            "full_context": full_context,
        }

        return context