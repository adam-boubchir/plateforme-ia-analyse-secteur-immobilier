from __future__ import annotations

from typing import Any

from app.agents.sql_agent.few_shot_provider import FewShotProvider

__all__ = ["PromptBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 80

QUESTION_ANALYSIS = "QUESTION ANALYSIS"
DATABASE_CONTEXT = "DATABASE CONTEXT"
FEW_SHOT_EXAMPLES = "FEW SHOT EXAMPLES"
USER_QUESTION = "USER QUESTION"
EXPECTED_OUTPUT = "EXPECTED OUTPUT"

DEFAULT_RULE_MESSAGE = "No specific business rules detected."
EXPECTED_SQL_OUTPUT = "Return ONLY the SQL query."


class PromptBuilder:
    """
    Build the final prompt sent to the SQL LLM.

    This class assembles:

        • System instructions
        • Dynamic rules
        • Database context
        • Few-shot examples
        • User question

    No business logic should be implemented here.
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

    def __init__(
        self,
        few_shot_provider: FewShotProvider,
    ) -> None:
        self.few_shot_provider = few_shot_provider

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_prompt(
        self,
        question: str,
        context: str,
        selection: dict[str, Any],
    ) -> str:
        """
        Build the final prompt sent to the LLM.
        """

        dynamic_rules = self._build_dynamic_rules(
            selection,
        )

        examples = self.few_shot_provider.get_examples(
            question,
        )

        sections = [
            self.SYSTEM_PROMPT,
            self._section(
                QUESTION_ANALYSIS,
                dynamic_rules,
            ),
            self._section(
                DATABASE_CONTEXT,
                context,
            ),
            self._section(
                FEW_SHOT_EXAMPLES,
                examples,
            ),
            self._section(
                USER_QUESTION,
                question,
            ),
            self._section(
                EXPECTED_OUTPUT,
                EXPECTED_SQL_OUTPUT,
            ),
            "SQL:",
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
        """
        Build one formatted prompt section.
        """

        return (
            f"{SECTION_SEPARATOR}\n"
            f"{title}\n"
            f"{SECTION_SEPARATOR}\n\n"
            f"{body}"
        )

    def _build_list_section(
        self,
        title: str,
        values: list[str],
        rules: list[str],
    ) -> None:
        """
        Add one formatted list section.
        """

        if not values:
            return

        rules.append(f"{title}:")

        rules.extend(
            f"• {value}"
            for value in values
        )

        rules.append("")

    def _add_aggregation_rules(
        self,
        rules: list[str],
    ) -> None:
        """
        Add aggregation instructions.
        """

        rules.extend(
            [
                "The query requires aggregation.",
                "Prefer AVG(), SUM(), COUNT(), MIN() or MAX().",
                "",
            ]
        )

    def _add_time_series_rules(
        self,
        rules: list[str],
    ) -> None:
        """
        Add temporal instructions.
        """

        rules.extend(
            [
                "The query is temporal.",
                "Always ORDER BY the chronological column.",
                "Use GROUP BY when appropriate.",
                "",
            ]
        )

    def _add_geographic_rules(
        self,
        rules: list[str],
    ) -> None:
        """
        Add geographic instructions.
        """

        rules.extend(
            [
                "Geographic dimensions are involved.",
                "Join REGION, PROVINCE_PREFECTURE or COMMUNE whenever required.",
                "",
            ]
        )

    def _add_join_rules(
        self,
        rules: list[str],
    ) -> None:
        """
        Add JOIN instructions.
        """

        rules.extend(
            [
                "Multiple tables are required.",
                "Generate explicit INNER JOIN statements.",
                "",
            ]
        )

    def _build_dynamic_rules(
        self,
        selection: dict[str, Any],
    ) -> str:
        """
        Build prompt instructions according
        to the detected question.
        """

        rules: list[str] = []

        self._build_list_section(
            "Business Domains",
            selection.get(
                "business_domains",
                [],
            ),
            rules,
        )

        self._build_list_section(
            "Question Types",
            selection.get(
                "question_types",
                [],
            ),
            rules,
        )

        self._build_list_section(
            "Selected Tables",
            selection.get(
                "tables",
                [],
            ),
            rules,
        )

        self._build_list_section(
            "Detected SQL Patterns",
            selection.get(
                "sql_patterns",
                [],
            ),
            rules,
        )

        if selection.get(
            "aggregation",
            False,
        ):
            self._add_aggregation_rules(
                rules,
            )

        if selection.get(
            "time_series",
            False,
        ):
            self._add_time_series_rules(
                rules,
            )

        if selection.get(
            "geographic",
            False,
        ):
            self._add_geographic_rules(
                rules,
            )

        if selection.get(
            "needs_join",
            False,
        ):
            self._add_join_rules(
                rules,
            )

        if not rules:
            rules.append(
                DEFAULT_RULE_MESSAGE,
            )

        return "\n".join(rules)