class BusinessRulesBuilder:
    """
    Build the business rules that help the LLM
    generate better SQL queries.
    """

    def build(
        self,
    ) -> list[str]:

        context = []

        context.append(
            "BUSINESS RULES"
        )

        context.append("")

        rules = [

            "The database contains Moroccan real estate data.",

            "All monetary values are expressed in Moroccan Dirham (MAD).",

            "Always use JOINs based on foreign keys.",

            "Never invent a table or a column.",

            "Never invent values that do not exist in the database.",

            "Prefer dimension tables to retrieve labels.",

            "Fact tables contain measures and indicators.",

            "Dimension tables contain descriptive information.",

            "Use semantic examples to identify filters.",

            "Use primary keys only for joins, never for display.",

            "Display business names instead of technical identifiers whenever possible.",

            "Never use SELECT *.",

            "Select only the useful columns.",

            "Use aggregates only when required by the question.",

            "Always generate valid SQL Server syntax.",

            "When a question contains a city, province or region name, use the semantic examples to identify the correct value.",

            "If the requested information does not exist in the database, return CANNOT_GENERATE_SQL."

        ]

        for index, rule in enumerate(
            rules,
            start=1,
        ):

            context.append(
                f"{index}. {rule}"
            )

        context.append("")

        context.append("=" * 100)

        context.append("")

        return context