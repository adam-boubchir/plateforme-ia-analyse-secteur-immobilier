from app.agents.sql_agent.patterns.sql_patterns import (
    SQLPatterns,
)


class SQLPatternBuilder:
    """
    Build the SQL Patterns section injected into the LLM prompt.

    This builder converts the selected SQL patterns into
    a structured prompt that guides the LLM toward generating
    high-quality SQL queries.
    """

    def __init__(
        self,
    ):

        self.patterns = SQLPatterns()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        question: str,
        selection: dict,
    ) -> list[str]:
        """
        Build the SQL Patterns section.
        """

        selected_patterns = self.patterns.get_patterns(

            question=question,

            selection=selection,

        )

        context = []

        context.append("=" * 100)
        context.append("")
        context.append("SQL PATTERNS")
        context.append("")

        if not selected_patterns:

            context.append(
                "No SQL patterns were selected."
            )

            context.append("")
            context.append("=" * 100)
            context.append("")

            return context

        context.append(
            f"Selected Patterns : {len(selected_patterns)}"
        )

        context.append("")

        for item in selected_patterns:

            context.extend(

                self._build_pattern(

                    pattern=item["pattern"],

                    score=item["score"],

                )

            )

        context.append("=" * 100)
        context.append("")

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_pattern(
        self,
        pattern: dict,
        score: int,
    ) -> list[str]:
        """
        Build one SQL pattern.
        """

        context = []

        context.append(
            f"Pattern : {pattern['name']}"
        )

        if pattern.get("category"):

            context.append(
                f"Category : {pattern['category']}"
            )

        context.append(
            f"Relevance Score : {score}"
        )

        context.append(
            f"Description : {pattern['description']}"
        )

        # --------------------------------------------------

        functions = pattern.get(
            "functions",
            [],
        )

        if functions:

            context.append("SQL Functions:")

            for function in functions:

                context.append(
                    f"  • {function}"
                )

        # --------------------------------------------------

        keywords = pattern.get(
            "keywords",
            [],
        )

        if keywords:

            context.append("Keywords:")

            for keyword in keywords:

                context.append(
                    f"  • {keyword}"
                )

        # --------------------------------------------------

        tables = pattern.get(
            "tables",
            [],
        )

        if tables:

            context.append("Recommended Tables:")

            for table in tables:

                context.append(
                    f"  • {table}"
                )

        # --------------------------------------------------

        context.append("Recommended SQL:")

        context.append(

            pattern["template"].strip()

        )

        # --------------------------------------------------

        recommendation = pattern.get(
            "recommendation",
            "",
        )

        if recommendation:

            context.append("Recommendation:")

            context.append(
                recommendation
            )

        context.append("")
        context.append("-" * 80)
        context.append("")

        return context