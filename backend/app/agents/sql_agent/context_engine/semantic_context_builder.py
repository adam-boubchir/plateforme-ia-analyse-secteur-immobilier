from app.services.semantic_context_service import (
    SemanticContextService,
)


class SemanticContextBuilder:
    """
    Build the semantic context that will be sent to the LLM.
    """

    def __init__(
        self,
        semantic_context_service: SemanticContextService,
    ):

        self.semantic_context_service = (
            semantic_context_service
        )

    def build(
        self,
        question: str,
    ) -> list[str]:
        """
        Build the semantic section.
        """

        context = []

        semantic_columns = (
            self.semantic_context_service.build(
                question
            )
        )

        if not semantic_columns:

            return []

        context.append(
            "SEMANTIC CONTEXT"
        )

        context.append("")

        for column in semantic_columns:

            context.extend(
                self._build_column(
                    column
                )
            )

        context.append(
            "=" * 100
        )

        context.append("")

        return context

    def _build_column(
        self,
        column: dict,
    ) -> list[str]:
        """
        Build one semantic column description.
        """

        context = []

        context.append(
            f"TABLE : {column['table']}"
        )

        context.append(
            f"COLUMN : {column['column']}"
        )

        if column.get(
            "semantic_type"
        ):

            context.append(
                f"Semantic Type : {column['semantic_type']}"
            )

        if column.get(
            "examples"
        ):

            context.append(
                "Examples :"
            )

            context.append(
                column["examples"]
            )

        if (
            column.get(
                "distinct_count"
            )
            is not None
        ):

            context.append(
                f"Distinct Values : {column['distinct_count']}"
            )

        if (
            column.get("min_value")
            is not None
            or column.get("max_value")
            is not None
        ):

            context.append(
                f"Range : {column['min_value']} -> {column['max_value']}"
            )

        if column.get(
            "is_primary_key"
        ):

            context.append(
                "Primary Key : YES"
            )

        if column.get(
            "is_foreign_key"
        ):

            context.append(
                "Foreign Key : YES"
            )

        if column.get(
            "score"
        ) is not None:

            context.append(
                f"Semantic Score : {column['score']}"
            )

        context.append("")

        return context