from __future__ import annotations

__all__ = ["HeaderBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 100

SECTION_TITLE = "DATABASE CONTEXT"
DATABASE_SECTION_TITLE = "DATABASE"

DATABASE_NAME = "OBSERVATOIRE_STAGIAIRE"
DATABASE_PURPOSE = "Moroccan Real Estate Observatory"
DATABASE_LANGUAGE = "French"
DATABASE_CURRENCY = "MAD"


class HeaderBuilder:
    """
    Build the database header section of the SQL context.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
    ) -> list[str]:
        """
        Build the database header section.
        """

        return [
            SECTION_SEPARATOR,
            SECTION_TITLE,
            SECTION_SEPARATOR,
            "",
            DATABASE_SECTION_TITLE,
            *self._build_database_information(),
            "",
            SECTION_SEPARATOR,
            "",
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_database_information(
        self,
    ) -> list[str]:
        """
        Build the database information.
        """

        return [
            f"Name : {DATABASE_NAME}",
            f"Purpose : {DATABASE_PURPOSE}",
            f"Language : {DATABASE_LANGUAGE}",
            f"Currency : {DATABASE_CURRENCY}",
        ]