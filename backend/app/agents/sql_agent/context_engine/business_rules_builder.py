from __future__ import annotations

__all__ = ["BusinessRulesBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_TITLE = "BUSINESS RULES"

SECTION_SEPARATOR = "=" * 100

BUSINESS_RULES: tuple[str, ...] = (
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
    (
        "Display business names instead of technical identifiers "
        "whenever possible."
    ),
    "Never use SELECT *.",
    "Select only the useful columns.",
    "Use aggregates only when required by the question.",
    "Always generate valid SQL Server syntax.",
    (
        "When a question contains a city, province or region name, "
        "use the semantic examples to identify the correct value."
    ),
    (
        "If the requested information does not exist in the database, "
        "return CANNOT_GENERATE_SQL."
    ),
)


class BusinessRulesBuilder:
    """
    Build the business rules section of the SQL context.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
    ) -> list[str]:
        """
        Build the business rules section.
        """

        return [
            SECTION_TITLE,
            "",
            *self._build_rules(),
            "",
            SECTION_SEPARATOR,
            "",
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_rules(
        self,
    ) -> list[str]:
        """
        Format all business rules.
        """

        return [
            f"{index}. {rule}"
            for index, rule in enumerate(
                BUSINESS_RULES,
                start=1,
            )
        ]