from __future__ import annotations

from typing import Any

from app.agents.sql_agent.few_shot_provider import (
    FewShotProvider,
)

__all__ = ("PromptBuilder",)

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
    Build the final prompt sent to the SQL language model.

    Responsibilities
    ----------------
    - Assemble the system prompt.
    - Build dynamic instructions.
    - Insert the database context.
    - Insert few-shot examples.
    - Produce the final prompt.
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

===========================================================
PREDICTION / FORECAST RULES
===========================================================

When the user asks for a prediction, forecast, projection,
future estimation, or similar future-oriented analysis:

1. SQL MUST ONLY retrieve the historical data required by
   the prediction agent.

2. NEVER perform the prediction or forecasting in SQL.

3. NEVER generate:
   - regression calculations
   - regression parameters
   - forecast years
   - future dates
   - predicted values
   - extrapolation formulas
   - trend-based future calculations

4. The prediction model is handled outside SQL by the
   Prediction Agent.

5. Return the historical time-series data needed by the
   Prediction Agent.

6. The result MUST contain:
   - the chronological column
   - the requested target variable
   - any filters explicitly requested by the user

7. Do not invent a target column.

8. Do not replace a requested price with an index or another
   metric unless the user explicitly asks for that metric.

9. If the requested target variable does not contain usable
   data in the selected tables, return:

CANNOT_GENERATE_SQL

10. A price request MUST use an actual price column such as
    prix_moyen when that column contains usable data.

11. NEVER use indice as a substitute for prix_moyen for a
    price prediction request.

12. If prix_moyen is unavailable or contains no usable values
    for the requested target, do not silently substitute
    indice.
"""

    def __init__(
        self,
        *,
        few_shot_provider: FewShotProvider,
    ) -> None:
        self._few_shot_provider = few_shot_provider

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_prompt(
        self,
        *,
        question: str,
        context: str,
        selection: dict[str, Any],
    ) -> str:
        """
        Build the final prompt sent to the SQL language model.

        Args:
            question:
                User natural-language question.

            context:
                Database context.

            selection:
                Knowledge selection.

        Returns:
            Complete prompt.
        """

        dynamic_rules = self._build_dynamic_rules(
            selection=selection,
        )

        examples = self._few_shot_provider.get_examples(
            question=question,
        )

        sections = [
            self.SYSTEM_PROMPT,
            self._section(
                title=QUESTION_ANALYSIS,
                body=dynamic_rules,
            ),
            self._section(
                title=DATABASE_CONTEXT,
                body=context,
            ),
            self._section(
                title=FEW_SHOT_EXAMPLES,
                body=examples,
            ),
            self._section(
                title=USER_QUESTION,
                body=question,
            ),
            self._section(
                title=EXPECTED_OUTPUT,
                body=EXPECTED_SQL_OUTPUT,
            ),
            "SQL:",
        ]

        prompt = "\n\n".join(
            sections,
        ).strip()

        return prompt

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _section(
        self,
        *,
        title: str,
        body: str,
    ) -> str:
        """
        Build one formatted prompt section.
        """

        section = (
            f"{SECTION_SEPARATOR}\n"
            f"{title}\n"
            f"{SECTION_SEPARATOR}\n\n"
            f"{body}"
        )

        return section

    def _build_list_section(
        self,
        *,
        title: str,
        values: list[str],
        rules: list[str],
    ) -> None:
        """
        Add one formatted list section.
        """

        if not values:
            return

        rules.append(
            f"{title}:",
        )

        rules.extend(
            f"• {value}"
            for value in values
        )

        rules.append(
            "",
        )

    @staticmethod
    def _add_aggregation_rules(
        *,
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

    @staticmethod
    def _add_time_series_rules(
        *,
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

    @staticmethod
    def _add_geographic_rules(
        *,
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

    @staticmethod
    def _add_join_rules(
        *,
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
        *,
        selection: dict[str, Any],
    ) -> str:
        """
        Build dynamic prompt instructions.

        Args:
            selection:
                Knowledge selection.

        Returns:
            Dynamic prompt instructions.
        """

        rules: list[str] = []

        self._build_list_section(
            title="Business Domains",
            values=selection.get(
                "business_domains",
                [],
            ),
            rules=rules,
        )

        self._build_list_section(
            title="Question Types",
            values=selection.get(
                "question_types",
                [],
            ),
            rules=rules,
        )

        self._build_list_section(
            title="Selected Tables",
            values=selection.get(
                "tables",
                [],
            ),
            rules=rules,
        )

        self._build_list_section(
            title="Detected SQL Patterns",
            values=selection.get(
                "sql_patterns",
                [],
            ),
            rules=rules,
        )

        if selection.get(
            "aggregation",
            False,
        ):
            self._add_aggregation_rules(
                rules=rules,
            )

        if selection.get(
            "time_series",
            False,
        ):
            self._add_time_series_rules(
                rules=rules,
            )

        if selection.get(
            "geographic",
            False,
        ):
            self._add_geographic_rules(
                rules=rules,
            )

        if selection.get(
            "needs_join",
            False,
        ):
            self._add_join_rules(
                rules=rules,
            )

        if not rules:
            rules.append(
                DEFAULT_RULE_MESSAGE,
            )

        dynamic_rules = "\n".join(
            rules,
        )

        return dynamic_rules