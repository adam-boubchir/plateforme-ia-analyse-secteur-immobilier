class ExamplesBuilder:
    """
    Build few-shot examples that help the LLM
    generate high quality SQL queries.
    """

    def build(
        self,
    ) -> list[str]:

        context = []

        context.append(
            "SQL EXAMPLES"
        )

        context.append("")

        examples = [

            {

                "question":
                "List all Moroccan regions.",

                "sql":
                """
SELECT
    nom_region
FROM REGION
ORDER BY nom_region;
                """.strip()

            },

            {

                "question":
                "Show the average price by region.",

                "sql":
                """
SELECT
    r.nom_region,
    AVG(f.prix_moyen) AS prix_moyen
FROM FACT_PRIX_INDICES f
INNER JOIN REGION r
    ON f.id_region = r.id_region
GROUP BY
    r.nom_region;
                """.strip()

            },

            {

                "question":
                "Average rent by housing type.",

                "sql":
                """
SELECT
    th.nom_type,
    AVG(l.loyer_moyen_mad) AS loyer_moyen
FROM LOYER_QUARTIER l
INNER JOIN TYPE_HABITAT th
    ON l.id_type_habitat = th.id_type_habitat
GROUP BY
    th.nom_type;
                """.strip()

            },

            {

                "question":
                "Average indicator by year.",

                "sql":
                """
SELECT
    annee,
    AVG(indice) AS moyenne
FROM FACT_INDICATEUR_HABITAT
GROUP BY
    annee
ORDER BY
    annee;
                """.strip()

            }

        ]

        for index, example in enumerate(
            examples,
            start=1,
        ):

            context.append(
                f"Example {index}"
            )

            context.append("")

            context.append(
                f"Question : {example['question']}"
            )

            context.append("")

            context.append(
                "SQL :"
            )

            context.append(
                example["sql"]
            )

            context.append("")

        context.append("=" * 100)

        context.append("")

        return context