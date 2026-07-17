from app.services.metadata_service import (
    MetadataService,
)


class RelationshipContextBuilder:
    """
    Build the DATABASE RELATIONSHIPS section of the SQL context.

    Only relationships involving the selected tables
    are included in the context.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
    ):

        self.metadata_service = (
            metadata_service
        )

    def build(
        self,
        selected_tables: list[str],
    ) -> list[str]:
        """
        Build the relationships section using only
        the selected tables.
        """

        context = []

        context.append(
            "DATABASE RELATIONSHIPS"
        )

        context.append("")

        relationships = [

            relationship

            for relationship in self.metadata_service.get_relationships()

            if (
                relationship.source_table in selected_tables
                and relationship.target_table in selected_tables
            )

        ]

        if not relationships:

            context.append(
                "No relationships found."
            )

            context.append("")

            context.append("=" * 100)

            context.append("")

            return context

        for relationship in relationships:

            context.extend(

                self._build_relationship(
                    relationship
                )

            )

        context.append(
            "=" * 100
        )

        context.append("")

        return context

    def _build_relationship(
        self,
        relationship,
    ) -> list[str]:
        """
        Build one relationship description.
        """

        context = []

        if hasattr(
            relationship,
            "constraint_name",
        ):

            context.append(
                f"Constraint : {relationship.constraint_name}"
            )

        context.append(
            f"{relationship.source_table}.{relationship.source_column}"
        )

        context.append(
            "        ↓"
        )

        context.append(
            f"{relationship.target_table}.{relationship.target_column}"
        )

        context.append("")

        return context