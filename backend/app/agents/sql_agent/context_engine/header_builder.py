from __future__ import annotations

__all__ = ("HeaderBuilder",)

# ==========================================================
# CONSTANTS
# ==========================================================

_SECTION_SEPARATOR = "=" * 100

_SECTION_TITLE = "DATABASE CONTEXT"
_DATABASE_SECTION_TITLE = "DATABASE"

_DATABASE_NAME = "OBSERVATOIRE_STAGIAIRE"
_DATABASE_PURPOSE = "Moroccan Real Estate Observatory"
_DATABASE_LANGUAGE = "French"
_DATABASE_CURRENCY = "MAD"


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

        Returns:
            List of formatted header lines.
        """

        return [
            _SECTION_SEPARATOR,
            _SECTION_TITLE,
            _SECTION_SEPARATOR,
            "",
            _DATABASE_SECTION_TITLE,
            *self._build_database_information(),
            "",
            _SECTION_SEPARATOR,
            "",
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_database_information() -> list[str]:
        """
        Build the database information block.

        Returns:
            List of database metadata lines.
        """

        return [
            f"Name : {_DATABASE_NAME}",
            f"Purpose : {_DATABASE_PURPOSE}",
            f"Language : {_DATABASE_LANGUAGE}",
            f"Currency : {_DATABASE_CURRENCY}",
        ]