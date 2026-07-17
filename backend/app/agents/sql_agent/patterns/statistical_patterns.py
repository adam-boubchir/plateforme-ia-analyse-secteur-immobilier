class StatisticalPatterns:
    """
    Collection of SQL statistical patterns.

    These patterns help the LLM answer
    statistical and analytical questions.
    """

    @staticmethod
    def get_patterns() -> list[dict]:

        return [

            {
                "name": "Average",

                "category": "Statistics",

                "intent": [
                    "average",
                    "moyenne",
                    "prix moyen",
                    "valeur moyenne",
                ],

                "description": (
                    "Compute an average value."
                ),

                "functions": [
                    "AVG",
                ],

                "keywords": [
                    "AVG",
                ],

                "template": """
SELECT
    AVG(metric)
FROM FACT_TABLE;
                """,

                "recommendation": (
                    "Use AVG() for average calculations."
                ),
            },

            {
                "name": "Minimum",

                "category": "Statistics",

                "intent": [
                    "minimum",
                    "plus petit",
                    "moins cher",
                ],

                "description": (
                    "Retrieve the minimum value."
                ),

                "functions": [
                    "MIN",
                ],

                "keywords": [
                    "MIN",
                ],

                "template": """
SELECT
    MIN(metric)
FROM FACT_TABLE;
                """,

                "recommendation": (
                    "Use MIN() for minimum values."
                ),
            },

            {
                "name": "Maximum",

                "category": "Statistics",

                "intent": [
                    "maximum",
                    "plus grand",
                    "plus cher",
                ],

                "description": (
                    "Retrieve the maximum value."
                ),

                "functions": [
                    "MAX",
                ],

                "keywords": [
                    "MAX",
                ],

                "template": """
SELECT
    MAX(metric)
FROM FACT_TABLE;
                """,

                "recommendation": (
                    "Use MAX() for maximum values."
                ),
            },

            {
                "name": "Percentage",

                "category": "Statistics",

                "intent": [
                    "pourcentage",
                    "percentage",
                    "part",
                    "ratio",
                ],

                "description": (
                    "Compute percentages."
                ),

                "functions": [
                    "COUNT",
                    "SUM",
                ],

                "keywords": [
                    "%",
                ],

                "template": """
SELECT
    category,
    COUNT(*) * 100.0 /
    SUM(COUNT(*)) OVER()
AS percentage
FROM FACT_TABLE
GROUP BY category;
                """,

                "recommendation": (
                    "Use window functions for percentages when available."
                ),
            },

            {
                "name": "Distribution",

                "category": "Statistics",

                "intent": [
                    "distribution",
                    "répartition",
                    "réparti",
                ],

                "description": (
                    "Analyse data distribution."
                ),

                "functions": [
                    "GROUP BY",
                    "COUNT",
                ],

                "keywords": [
                    "GROUP BY",
                ],

                "template": """
SELECT
    category,
    COUNT(*)
FROM FACT_TABLE
GROUP BY category;
                """,

                "recommendation": (
                    "Group values before counting."
                ),
            },

            {
                "name": "Variance",

                "category": "Statistics",

                "intent": [
                    "variance",
                    "dispersion",
                ],

                "description": (
                    "Compute variance."
                ),

                "functions": [
                    "VAR",
                ],

                "keywords": [
                    "VAR",
                ],

                "template": """
SELECT
    VAR(metric)
FROM FACT_TABLE;
                """,

                "recommendation": (
                    "Use only if supported by SQL Server."
                ),
            },

            {
                "name": "Standard Deviation",

                "category": "Statistics",

                "intent": [
                    "écart type",
                    "standard deviation",
                ],

                "description": (
                    "Compute standard deviation."
                ),

                "functions": [
                    "STDEV",
                ],

                "keywords": [
                    "STDEV",
                ],

                "template": """
SELECT
    STDEV(metric)
FROM FACT_TABLE;
                """,

                "recommendation": (
                    "Useful for variability analysis."
                ),
            },

        ]