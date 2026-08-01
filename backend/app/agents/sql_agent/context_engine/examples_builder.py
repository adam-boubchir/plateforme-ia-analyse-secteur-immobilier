# ==========================================================
# CONSTANTS
# ==========================================================

SECTION_SEPARATOR = "=" * 100

SQL_EXAMPLES = [
    {
        "question": "List all Moroccan regions.",
        "sql": """
SELECT
    nom_region
FROM REGION
ORDER BY nom_region;
""".strip(),
    },
    {
        "question": "Show the average price by region.",
        "sql": """
SELECT
    r.nom_region,
    AVG(f.prix_moyen) AS prix_moyen
FROM FACT_PRIX_INDICES f
INNER JOIN REGION r
    ON f.id_region = r.id_region
GROUP BY
    r.nom_region;
""".strip(),
    },
    {
        "question": "Average rent by housing type.",
        "sql": """
SELECT
    th.nom_type,
    AVG(l.loyer_moyen_mad) AS loyer_moyen
FROM LOYER_QUARTIER l
INNER JOIN TYPE_HABITAT th
    ON l.id_type_habitat = th.id_type_habitat
GROUP BY
    th.nom_type;
""".strip(),
    },
    {
        "question": "Average indicator by year.",
        "sql": """
SELECT
    annee,
    AVG(indice) AS moyenne
FROM FACT_INDICATEUR_HABITAT
GROUP BY
    annee
ORDER BY
    annee;
""".strip(),
    },
]


class ExamplesBuilder:
    """
    Build few-shot examples that help the LLM
    generate high-quality SQL queries.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
    ) -> list[str]:
        """
        Build the SQL examples section.
        """

        context = [
            "SQL EXAMPLES",
            "",
        ]

        for index, example in enumerate(
            SQL_EXAMPLES,
            start=1,
        ):
            context.extend(
                self._build_example(
                    index=index,
                    example=example,
                )
            )

        context.extend(
            [
                SECTION_SEPARATOR,
                "",
            ]
        )

        return context

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_example(
        self,
        index: int,
        example: dict[str, str],
    ) -> list[str]:
        """
        Build one SQL example.
        """

        return [
            f"Example {index}",
            "",
            f"Question : {example['question']}",
            "",
            "SQL :",
            example["sql"],
            "",
        ]