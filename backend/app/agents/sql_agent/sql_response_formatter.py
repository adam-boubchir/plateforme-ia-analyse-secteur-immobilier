from __future__ import annotations

from typing import Any

__all__ = ["SQLResponseFormatter"]

# ==========================================================
# CONSTANTS
# ==========================================================

EMPTY_RESULT_MESSAGE = (
    "Aucune donnée ne correspond à votre demande."
)

SINGLE_RESULT_MESSAGE = (
    "Votre requête a retourné un seul résultat.\n\n"
    "Les informations sont disponibles dans le tableau des résultats."
)

MULTIPLE_RESULTS_TEMPLATE = (
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

    This class does not interpret SQL data.
    It only summarizes the execution outcome.

    Natural-language explanations should be produced
    by a dedicated Response Agent.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def format(
        self,
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Build a user-friendly summary of the SQL execution.
        """

        row_count = len(rows)

        if row_count == 0:
            return self._empty_result()

        if row_count == 1:
            return self._single_result()

        return self._multiple_results(
            row_count,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _empty_result(self) -> str:
        """
        Return the message displayed when no rows are returned.
        """

        return EMPTY_RESULT_MESSAGE

    def _single_result(self) -> str:
        """
        Return the message displayed for a single row.
        """

        return SINGLE_RESULT_MESSAGE

    def _multiple_results(
        self,
        row_count: int,
    ) -> str:
        """
        Return the message displayed for multiple rows.
        """

        return MULTIPLE_RESULTS_TEMPLATE.format(
            total=row_count,
        )