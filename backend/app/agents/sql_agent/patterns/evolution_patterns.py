class EvolutionPatterns:
    """
    Collection of SQL evolution patterns.

    These patterns help the LLM generate
    time-series SQL queries.
    """

    @staticmethod
    def get_patterns() -> list[dict]:

        return [

            {
                "name": "Yearly Evolution",

                "category": "Evolution",

                "intent": [
                    "évolution",
                    "evolution",
                    "trend",
                    "tendance",
                    "historique",
                    "au fil du temps",
                ],

                "description": (
                    "Retrieve the evolution of a metric over time."
                ),

                "functions": [
                    "GROUP BY",
                    "ORDER BY",
                ],

                "keywords": [
                    "annee",
                    "GROUP BY",
                    "ORDER BY",
                ],

                "template": """
SELECT
    annee,
    AVG(metric)
FROM FACT_TABLE
GROUP BY annee
ORDER BY annee;
                """,

                "recommendation": (
                    "Always sort chronologically."
                ),
            },

            {
                "name": "Evolution Between Two Years",

                "category": "Evolution",

                "intent": [
                    "entre",
                    "between",
                    "de",
                    "à",
                    "from",
                    "to",
                ],

                "description": (
                    "Retrieve the evolution between two years."
                ),

                "functions": [
                    "BETWEEN",
                    "GROUP BY",
                ],

                "keywords": [
                    "BETWEEN",
                    "annee",
                ],

                "template": """
SELECT
    annee,
    AVG(metric)
FROM FACT_TABLE
WHERE annee BETWEEN 2015 AND 2024
GROUP BY annee
ORDER BY annee;
                """,

                "recommendation": (
                    "Use BETWEEN when a period is specified."
                ),
            },

            {
                "name": "Monthly Evolution",

                "category": "Evolution",

                "intent": [
                    "mois",
                    "mensuel",
                    "monthly",
                ],

                "description": (
                    "Retrieve the monthly evolution."
                ),

                "functions": [
                    "GROUP BY",
                    "ORDER BY",
                ],

                "keywords": [
                    "mois",
                    "month",
                ],

                "template": """
SELECT
    mois,
    AVG(metric)
FROM FACT_TABLE
GROUP BY mois
ORDER BY mois;
                """,

                "recommendation": (
                    "Keep chronological ordering."
                ),
            },

            {
                "name": "Evolution by Region",

                "category": "Evolution",

                "intent": [
                    "évolution par région",
                    "par région",
                    "region",
                ],

                "description": (
                    "Retrieve yearly evolution grouped by region."
                ),

                "functions": [
                    "JOIN",
                    "GROUP BY",
                ],

                "keywords": [
                    "REGION",
                    "GROUP BY",
                ],

                "template": """
SELECT
    r.nom_region,
    annee,
    AVG(metric)
FROM FACT_TABLE f
INNER JOIN REGION r
ON f.id_region = r.id_region
GROUP BY
    r.nom_region,
    annee
ORDER BY
    annee;
                """,

                "recommendation": (
                    "Join the geographic dimension before grouping."
                ),
            },

            {
                "name": "Evolution by Category",

                "category": "Evolution",

                "intent": [
                    "par matériau",
                    "par type",
                    "par catégorie",
                    "catégorie",
                ],

                "description": (
                    "Retrieve the evolution for each category."
                ),

                "functions": [
                    "GROUP BY",
                ],

                "keywords": [
                    "GROUP BY",
                ],

                "template": """
SELECT
    category,
    annee,
    AVG(metric)
FROM FACT_TABLE
GROUP BY
    category,
    annee
ORDER BY
    annee;
                """,

                "recommendation": (
                    "Group both category and year."
                ),
            },

        ]