from __future__ import annotations

__all__ = ("PromptRulesBuilder",)

# ==========================================================
# CONSTANTS
# ==========================================================

_SECTION_TITLE = "SQL GENERATION RULES"

_SECTION_SEPARATOR = "=" * 100

_PROMPT_RULES: tuple[str, ...] = (
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
    (
        "If the question cannot be answered from the available schema, "
        "return exactly CANNOT_GENERATE_SQL."
    ),
)


class PromptRulesBuilder:
    """
    Build the SQL generation rules section of the SQL context.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
    ) -> list[str]:
        """
        Build the SQL generation rules section.

        Returns:
            List of formatted SQL generation rules.
        """

        return [
            _SECTION_TITLE,
            "",
            *self._build_rules(),
            "",
            _SECTION_SEPARATOR,
            "",
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_rules() -> list[str]:
        """
        Format all SQL generation rules.

        Returns:
            Numbered list of SQL generation rules.
        """

        return [
            f"{index}. {rule}"
            for index, rule in enumerate(
                _PROMPT_RULES,
                start=1,
            )
        ]