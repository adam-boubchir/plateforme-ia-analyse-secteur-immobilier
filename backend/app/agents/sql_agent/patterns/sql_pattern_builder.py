from app.agents.sql_agent.patterns.sql_patterns import (
    SQLPatterns,
)

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 100
PATTERN_SEPARATOR = "-" * 80


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

        context = [
            SECTION_SEPARATOR,
            "",
            "SQL PATTERNS",
            "",
        ]

        if not selected_patterns:
            context.extend(
                self._build_empty_section()
            )
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

        context.extend(
            [
                SECTION_SEPARATOR,
                "",
            ]
        )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_empty_section(
        self,
    ) -> list[str]:
        """
        Build the empty SQL pattern section.
        """

        return [
            "No SQL patterns were selected.",
            "",
            SECTION_SEPARATOR,
            "",
        ]

    def _build_pattern(
        self,
        pattern: dict,
        score: int,
    ) -> list[str]:
        """
        Build one SQL pattern.
        """

        context = [
            f"Pattern : {pattern.get('name', '')}",
        ]

        category = pattern.get(
            "category",
        )

        if category:
            context.append(
                f"Category : {category}"
            )

        context.append(
            f"Relevance Score : {score}"
        )

        context.append(
            f"Description : {pattern.get('description', '')}"
        )

        context.extend(
            self._build_list_section(
                "SQL Functions",
                pattern.get(
                    "functions",
                    [],
                ),
            )
        )

        context.extend(
            self._build_list_section(
                "Keywords",
                pattern.get(
                    "keywords",
                    [],
                ),
            )
        )

        context.extend(
            self._build_list_section(
                "Recommended Tables",
                pattern.get(
                    "tables",
                    [],
                ),
            )
        )

        context.append(
            "Recommended SQL:"
        )

        context.append(
            pattern.get(
                "template",
                "",
            ).strip()
        )

        recommendation = pattern.get(
            "recommendation",
        )

        if recommendation:
            context.append(
                "Recommendation:"
            )

            context.append(
                recommendation
            )

        context.extend(
            [
                "",
                PATTERN_SEPARATOR,
                "",
            ]
        )

        return context

    def _build_list_section(
        self,
        title: str,
        values: list[str],
    ) -> list[str]:
        """
        Build a generic list section.
        """

        if not values:
            return []

        return [
            title + ":",
            *[
                f"  • {value}"
                for value in values
            ],
        ]