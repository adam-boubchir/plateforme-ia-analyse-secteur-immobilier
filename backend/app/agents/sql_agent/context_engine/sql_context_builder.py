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


class SQLContextBuilder:
    """
    Professional SQL Context Engine.

    Responsible for building every section of the
    SQL context sent to the LLM.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
        semantic_context_service: SemanticContextService,
    ):

        self.header_builder = HeaderBuilder()

        self.business_knowledge_builder = (
            BusinessKnowledgeBuilder()
        )

        self.join_knowledge_builder = (
            JoinKnowledgeBuilder()
        )

        self.forbidden_join_builder = (
            ForbiddenJoinBuilder()
        )

        self.business_rules_builder = (
            BusinessRulesBuilder()
        )

        self.sql_pattern_builder = (
            SQLPatternBuilder()
        )

        self.table_builder = (
            TableContextBuilder(
                metadata_service
            )
        )

        self.relationship_builder = (
            RelationshipContextBuilder(
                metadata_service
            )
        )

        self.semantic_builder = (
            SemanticContextBuilder(
                semantic_context_service
            )
        )

        self.prompt_rules_builder = (
            PromptRulesBuilder()
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_context(
        self,
        question: str,
        selection: dict,
    ) -> dict:
        """
        Build every context section independently
        and also return the complete context.
        """

        selected_tables = selection["tables"]

        print("\n")
        print("=" * 100)
        print("KNOWLEDGE SELECTION")
        print("=" * 100)
        print(selection)
        print("=" * 100)
        print("\n")

        # ------------------------------------------------------
        # Build every section
        # ------------------------------------------------------

        header = self.header_builder.build()

        business = self.business_knowledge_builder.build(
            selected_tables
        )

        joins = self.join_knowledge_builder.build(
            selected_tables
        )

        forbidden = self.forbidden_join_builder.build(
            selected_tables
        )

        business_rules = self.business_rules_builder.build()

        sql_patterns = self.sql_pattern_builder.build(
            question=question,
            selection=selection,
        )

        tables = self.table_builder.build(
            selected_tables
        )

        relationships = self.relationship_builder.build(
            selected_tables
        )

        semantic = self.semantic_builder.build(
            question
        )

        prompt_rules = self.prompt_rules_builder.build()

        # ------------------------------------------------------
        # Full context
        # ------------------------------------------------------

        context = []

        context.extend(header)
        context.extend(business)
        context.extend(joins)
        context.extend(forbidden)
        context.extend(business_rules)
        context.extend(sql_patterns)
        context.extend(tables)
        context.extend(relationships)
        context.extend(semantic)
        context.extend(prompt_rules)

        full_context = "\n".join(context)

        print("\n")
        print("=" * 100)
        print("SQL CONTEXT")
        print("=" * 100)
        print(full_context)
        print("=" * 100)
        print("\n")

        print("=" * 100)
        print("BUSINESS KNOWLEDGE")
        print("\n".join(business))

        print("=" * 100)
        print("JOIN KNOWLEDGE")
        print("\n".join(joins))

        print("=" * 100)
        print("FORBIDDEN JOINS")
        print("\n".join(forbidden))

        print("=" * 100)
        print("SEMANTIC CONTEXT")
        print("\n".join(semantic))

        return {

            "business_knowledge": "\n".join(
                business
            ),

            "join_knowledge": "\n".join(
                joins
            ),

            "forbidden_joins": "\n".join(
                forbidden
            ),

            "semantic_context": "\n".join(
                semantic
            ),

            "sql_patterns": "\n".join(
                sql_patterns
            ),

            "full_context": full_context,

        }