from app.agents.sql_agent.few_shot_provider import (
    FewShotProvider,
)


class PromptBuilder:
    """
    Builds the final prompt sent to the SQL LLM.

    The PromptBuilder combines:

        • System instructions
        • Dynamic rules inferred from the question
        • Database context
        • Few-shot examples
        • User question

    This class should contain NO business logic.
    """

    SYSTEM_PROMPT = """
You are an expert Microsoft SQL Server engineer specialized in Text-to-SQL.

Your mission is to generate the most accurate Microsoft SQL Server query possible.

===========================================================
GENERAL RULES
===========================================================

1. Return ONLY SQL.
2. Never explain your answer.
3. Never use Markdown.
4. Never wrap the SQL inside ```sql.
5. Never invent tables.
6. Never invent columns.
7. Use ONLY the provided schema.
8. Use Microsoft SQL Server syntax.
9. Generate ONLY SELECT queries.
10. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, EXEC, MERGE or TRUNCATE.
11. Never use SELECT *.
12. Select only the necessary columns.
13. Always use aliases.
14. Use explicit JOIN conditions.
15. Use INNER JOIN whenever relationships exist.
16. Use GROUP BY correctly.
17. Use ORDER BY whenever chronology or ranking is expected.
18. Prefer efficient SQL.
19. Never ignore business rules.
20. Respect forbidden joins.
21. If the answer cannot be generated using the provided schema,
return exactly:

CANNOT_GENERATE_SQL

Nothing else.
"""

    def __init__(self):

        self.few_shot_provider = FewShotProvider()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_prompt(
        self,
        question: str,
        context: str,
        selection: dict,
    ) -> str:
        """
        Build the final LLM prompt.
        """

        dynamic_rules = self._build_dynamic_rules(
            selection
        )

        examples = self.few_shot_provider.get_examples(
            question
        )

        sections = [

            self.SYSTEM_PROMPT,

            self._section(
                "QUESTION ANALYSIS",
                dynamic_rules,
            ),

            self._section(
                "DATABASE CONTEXT",
                context,
            ),

            self._section(
                "FEW SHOT EXAMPLES",
                examples,
            ),

            self._section(
                "USER QUESTION",
                question,
            ),

            self._section(
                "EXPECTED OUTPUT",
                "Return ONLY the SQL query.",
            ),

            "SQL:"
        ]

        return "\n\n".join(sections).strip()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _section(
        self,
        title: str,
        body: str,
    ) -> str:

        return (
            "=" * 80
            + "\n"
            + title
            + "\n"
            + "=" * 80
            + "\n\n"
            + body
        )

    def _build_dynamic_rules(
        self,
        selection: dict,
    ) -> str:
        """
        Build dynamic prompt instructions according
        to the detected question.
        """

        rules = []

        # ------------------------------------------------------
        # Business domains
        # ------------------------------------------------------

        business_domains = selection.get(
            "business_domains",
            [],
        )

        if business_domains:

            rules.append(
                "Business Domains:"
            )

            for domain in business_domains:

                rules.append(
                    f"• {domain}"
                )

            rules.append("")

        # ------------------------------------------------------
        # Question types
        # ------------------------------------------------------

        question_types = selection.get(
            "question_types",
            [],
        )

        if question_types:

            rules.append(
                "Question Types:"
            )

            for q in question_types:

                rules.append(
                    f"• {q}"
                )

            rules.append("")

        # ------------------------------------------------------
        # Selected tables
        # ------------------------------------------------------

        tables = selection.get(
            "tables",
            [],
        )

        if tables:

            rules.append(
                "Selected Tables:"
            )

            for table in tables:

                rules.append(
                    f"• {table}"
                )

            rules.append("")

        # ------------------------------------------------------
        # SQL Patterns
        # ------------------------------------------------------

        patterns = selection.get(
            "sql_patterns",
            [],
        )

        if patterns:

            rules.append(
                "Detected SQL Patterns:"
            )

            for pattern in patterns:

                rules.append(
                    f"• {pattern}"
                )

            rules.append("")

        # ------------------------------------------------------
        # Aggregation
        # ------------------------------------------------------

        if selection.get(
            "aggregation",
            False,
        ):

            rules.append(
                "The query requires aggregation."
            )

            rules.append(
                "Prefer AVG(), SUM(), COUNT(), MIN() or MAX()."
            )

            rules.append("")

        # ------------------------------------------------------
        # Time Series
        # ------------------------------------------------------

        if selection.get(
            "time_series",
            False,
        ):

            rules.append(
                "The query is temporal."
            )

            rules.append(
                "Always ORDER BY the chronological column."
            )

            rules.append(
                "Use GROUP BY when appropriate."
            )

            rules.append("")

        # ------------------------------------------------------
        # Geographic
        # ------------------------------------------------------

        if selection.get(
            "geographic",
            False,
        ):

            rules.append(
                "Geographic dimensions are involved."
            )

            rules.append(
                "Join REGION, PROVINCE_PREFECTURE or COMMUNE whenever required."
            )

            rules.append("")

        # ------------------------------------------------------
        # Join
        # ------------------------------------------------------

        if selection.get(
            "needs_join",
            False,
        ):

            rules.append(
                "Multiple tables are required."
            )

            rules.append(
                "Generate explicit INNER JOIN statements."
            )

            rules.append("")

        if not rules:

            rules.append(
                "No specific business rules detected."
            )

        return "\n".join(rules)