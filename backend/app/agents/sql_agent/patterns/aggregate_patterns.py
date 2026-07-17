class AggregatePatterns:
    """
    Collection of SQL aggregation patterns.
    """

    @staticmethod
    def get_patterns() -> list[dict]:
        """
        Return aggregation SQL patterns.
        """

        return [

            {
                "name": "Average",

                "category": "Aggregate",

                "intent": [
                    "average",
                    "avg",
                    "mean",
                    "prix moyen",
                    "moyenne",
                ],

                "description":
                    "Compute the average value of a numeric column.",

                "functions": [
                    "AVG"
                ],

                "keywords": [
                    "average",
                    "avg",
                    "moyenne",
                    "prix moyen",
                ],

                "template": """
SELECT
    AVG(column_name) AS average_value
FROM table_name
WHERE conditions;
                """,

                "recommendation":
                    "Use AVG() only on numeric columns.",
            },

            {
                "name": "Count",

                "category": "Aggregate",

                "intent": [
                    "count",
                    "combien",
                    "nombre",
                    "total",
                ],

                "description":
                    "Count the number of rows.",

                "functions": [
                    "COUNT"
                ],

                "keywords": [
                    "count",
                    "combien",
                    "nombre",
                    "total",
                ],

                "template": """
SELECT
    COUNT(*) AS total_rows
FROM table_name
WHERE conditions;
                """,

                "recommendation":
                    "COUNT(*) is preferred when counting rows.",
            },

            {
                "name": "Sum",

                "category": "Aggregate",

                "intent": [
                    "sum",
                    "total",
                    "somme",
                ],

                "description":
                    "Calculate the sum of a numeric column.",

                "functions": [
                    "SUM"
                ],

                "keywords": [
                    "sum",
                    "total",
                    "somme",
                ],

                "template": """
SELECT
    SUM(column_name) AS total
FROM table_name
WHERE conditions;
                """,

                "recommendation":
                    "Use SUM() only with numeric values.",
            },

            {
                "name": "Minimum",

                "category": "Aggregate",

                "intent": [
                    "minimum",
                    "min",
                    "plus petit",
                    "moins cher",
                ],

                "description":
                    "Retrieve the smallest value.",

                "functions": [
                    "MIN"
                ],

                "keywords": [
                    "minimum",
                    "min",
                    "moins cher",
                ],

                "template": """
SELECT
    MIN(column_name) AS minimum_value
FROM table_name
WHERE conditions;
                """,

                "recommendation":
                    "Useful for lowest prices and earliest dates.",
            },

            {
                "name": "Maximum",

                "category": "Aggregate",

                "intent": [
                    "maximum",
                    "max",
                    "plus grand",
                    "plus cher",
                ],

                "description":
                    "Retrieve the largest value.",

                "functions": [
                    "MAX"
                ],

                "keywords": [
                    "maximum",
                    "max",
                    "plus cher",
                ],

                "template": """
SELECT
    MAX(column_name) AS maximum_value
FROM table_name
WHERE conditions;
                """,

                "recommendation":
                    "Useful for highest prices and latest dates.",
            },

        ]