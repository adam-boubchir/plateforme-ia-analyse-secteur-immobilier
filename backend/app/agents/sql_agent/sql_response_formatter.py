from typing import Any


class SQLResponseFormatter:
    """
    Format SQL query results into a user-friendly response.

    This class does NOT interpret data.
    It only summarizes the execution result.

    Later a dedicated Response Agent can transform
    SQL results into natural language.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def format(
        self,
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Format SQL results.
        """

        total = len(rows)

        if total == 0:

            return self._empty_result()

        if total == 1:

            return self._single_result()

        return self._multiple_results(
            total
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _empty_result(
        self,
    ) -> str:

        return (
            "Aucune donnée ne correspond à votre demande."
        )

    def _single_result(
        self,
    ) -> str:

        return (
            "Votre requête a retourné un seul résultat.\n\n"
            "Les informations sont disponibles dans le tableau des résultats."
        )

    def _multiple_results(
        self,
        total: int,
    ) -> str:

        return (
            f"La requête SQL a retourné {total} résultats.\n\n"
            "Les données sont affichées dans le tableau.\n\n"
            "Vous pouvez :\n"
            "• trier les colonnes ;\n"
            "• filtrer les données ;\n"
            "• rechercher des valeurs ;\n"
            "• exporter les résultats ;\n"
            "• utiliser les visualisations disponibles."
        )