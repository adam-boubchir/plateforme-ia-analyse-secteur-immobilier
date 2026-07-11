class SQLResponseFormatter:
    """
    Format SQL query results into a human-readable response.
    """

    def format(
        self,
        rows: list[dict],
    ) -> str:

        total = len(rows)

        if total == 0:

            return (
                "Aucune donnée ne correspond à votre demande."
            )

        if total == 1:

            return (
                "Votre requête a retourné un seul résultat. "
                "Les informations détaillées sont disponibles dans le tableau ci-dessous."
            )

        return (
            f"Votre requête a retourné **{total} résultats**.\n\n"
            "Les données sont présentées dans le tableau ci-dessous.\n\n"
            "Vous pouvez :\n"
            "• consulter les indicateurs générés automatiquement ;\n"
            "• explorer la visualisation lorsqu'elle est disponible ;\n"
            "• rechercher, trier et filtrer les données ;\n"
            "• exporter les résultats au format CSV."
        )