class PromptRulesBuilder:
    """
    Build the prompt instructions that the SQL LLM
    must always follow.
    """

    def build(
        self,
    ) -> list[str]:

        context = []

        context.append(
            "SQL GENERATION RULES"
        )

        context.append("")

        rules = [

            "Generate ONLY one SQL query.",

            "Return ONLY SQL.",

            "Do not explain the query.",

            "Do not use Markdown.",

            "Do not surround SQL with ```sql.",

            "Never invent tables.",

            "Never invent columns.",

            "Never invent values.",

            "Respect foreign key relationships.",

            "Prefer explicit INNER JOIN.",

            "Use aliases when appropriate.",

            "Use GROUP BY only when aggregation is requested.",

            "Use ORDER BY when it improves readability.",

            "Never use SELECT *.",

            "Select only the required columns.",

            "Always generate SQL Server syntax.",

            "If the question cannot be answered from the available schema, return exactly CANNOT_GENERATE_SQL."

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