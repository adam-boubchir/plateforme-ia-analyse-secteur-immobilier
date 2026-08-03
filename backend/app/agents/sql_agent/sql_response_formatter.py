from __future__ import annotations

from typing import Any

__all__ = ("SQLResponseFormatter",)

# ==========================================================
# CONSTANTS
# ==========================================================

_EMPTY_RESULT_MESSAGE = (
    "Aucune donnée ne correspond à votre demande."
)

_SINGLE_RESULT_MESSAGE = (
    "Votre requête a retourné un seul résultat.\n\n"
    "Les informations sont disponibles dans le tableau des résultats."
)

_MULTIPLE_RESULTS_TEMPLATE = (
    "La requête SQL a retourné {total} résultats.\n\n"
    "Les données sont affichées dans le tableau.\n\n"
    "Vous pouvez :\n"
    "• Trier les colonnes ;\n"
    "• Filtrer les données ;\n"
    "• Rechercher des valeurs ;\n"
    "• Exporter les résultats ;\n"
    "• Utiliser les visualisations disponibles."
)


class SQLResponseFormatter:
    """
    Format SQL execution results.

    Responsibilities
    ----------------
    - Summarize the SQL execution result.
    - Produce a user-friendly message.
    - Avoid interpreting SQL data.

    Natural-language explanations should be produced
    by a dedicated Response Agent.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def format(
        self,
        *,
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Build a summary of the SQL execution.

        Args:
            rows:
                SQL query result.

        Returns:
            User-friendly summary.
        """

        row_count = len(
            rows,
        )

        if row_count == 0:
            message = self._empty_result()
            return message

        if row_count == 1:
            message = self._single_result()
            return message

        message = self._multiple_results(
            row_count=row_count,
        )

        return message

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _empty_result() -> str:
        """
        Return the message displayed when no rows are returned.
        """

        message = _EMPTY_RESULT_MESSAGE

        return message

    @staticmethod
    def _single_result() -> str:
        """
        Return the message displayed when exactly one row is returned.
        """

        message = _SINGLE_RESULT_MESSAGE

        return message

    @staticmethod
    def _multiple_results(
        *,
        row_count: int,
    ) -> str:
        """
        Return the message displayed when multiple rows are returned.
        """

        message = _MULTIPLE_RESULTS_TEMPLATE.format(
            total=row_count,
        )

        return message