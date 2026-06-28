class SQLResponseFormatter:
    """
    Format SQL query results into a human-readable response.
    """

    MAX_ROWS = 100

    def format(
        self,
        rows: list[dict],
    ) -> str:

        if not rows:

            return "Aucun résultat trouvé."

        total = len(rows)

        displayed_rows = rows[: self.MAX_ROWS]

        lines = []

        lines.append(
            f"{total} résultat(s) trouvé(s)."
        )

        lines.append("")

        for index, row in enumerate(displayed_rows, start=1):

            lines.append(f"Ligne {index}")

            for key, value in row.items():

                lines.append(
                    f"  {key} : {value}"
                )

            lines.append("")

        if total > self.MAX_ROWS:

            lines.append(
                f"... {total - self.MAX_ROWS} ligne(s) supplémentaire(s) non affichée(s)."
            )

        return "\n".join(lines)