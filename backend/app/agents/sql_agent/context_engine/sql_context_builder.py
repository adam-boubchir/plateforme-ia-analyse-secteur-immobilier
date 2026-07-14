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

from .business_rules_builder import (
    BusinessRulesBuilder,
)

from .examples_builder import (
    ExamplesBuilder,
)

from .prompt_rules_builder import (
    PromptRulesBuilder,
)


class SQLContextBuilder:
    """
    Professional SQL Context Engine.

    This class orchestrates every builder responsible
    for generating the context sent to the LLM.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
        semantic_context_service: SemanticContextService,
    ):

        self.header_builder = (
            HeaderBuilder()
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

        self.business_builder = (
            BusinessRulesBuilder()
        )

        self.examples_builder = (
            ExamplesBuilder()
        )

        self.prompt_rules_builder = (
            PromptRulesBuilder()
        )

    def build_context(
        self,
        question: str,
    ) -> str:
        """
        Build the complete context.
        """

        context = []

        context.extend(
            self.header_builder.build()
        )

        context.extend(
            self.business_builder.build()
        )

        context.extend(
            self.table_builder.build()
        )

        context.extend(
            self.relationship_builder.build()
        )

        context.extend(
            self.semantic_builder.build(
                question
            )
        )

        context.extend(
            self.examples_builder.build()
        )

        context.extend(
            self.prompt_rules_builder.build()
        )

        context_string = "\n".join(
            context
        )

        print("\n")
        print("=" * 100)
        print("SQL CONTEXT")
        print("=" * 100)
        print(context_string)
        print("=" * 100)
        print("\n")

        return context_string