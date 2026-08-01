# ==========================================================
# CONSTANTS
# ==========================================================

RANKING_PATTERNS = [
    {
        "name": "Top N",
        "category": "Ranking",
        "intent": [
            "top",
            "top 5",
            "top 10",
            "highest",
            "best",
            "plus cher",
            "plus élevé",
            "les meilleurs",
        ],
        "description": (
            "Retrieve the first N records ordered by a metric."
        ),
        "functions": [
            "TOP",
            "ORDER BY",
            "DESC",
        ],
        "keywords": [
            "TOP",
            "DESC",
            "ORDER BY",
        ],
        "template": """
SELECT TOP (10)
    column_name,
    metric
FROM table_name
ORDER BY
    metric DESC;
""".strip(),
        "recommendation": (
            "Always combine TOP with ORDER BY DESC."
        ),
    },
    {
        "name": "Bottom N",
        "category": "Ranking",
        "intent": [
            "bottom",
            "moins cher",
            "lowest",
            "smallest",
        ],
        "description": (
            "Retrieve the smallest values."
        ),
        "functions": [
            "TOP",
            "ORDER BY",
            "ASC",
        ],
        "keywords": [
            "TOP",
            "ASC",
            "ORDER BY",
        ],
        "template": """
SELECT TOP (10)
    column_name,
    metric
FROM table_name
ORDER BY
    metric ASC;
""".strip(),
        "recommendation": (
            "Use ASC when searching for the smallest values."
        ),
    },
    {
        "name": "Ordered Result",
        "category": "Ranking",
        "intent": [
            "order",
            "sorted",
            "classer",
            "trier",
        ],
        "description": (
            "Sort records using ORDER BY."
        ),
        "functions": [
            "ORDER BY",
        ],
        "keywords": [
            "ORDER BY",
        ],
        "template": """
SELECT
    *
FROM table_name
ORDER BY
    column_name;
""".strip(),
        "recommendation": (
            "Sorting should be explicit."
        ),
    },
]


class RankingPatterns:
    """
    Collection of SQL ranking patterns.

    These patterns help the LLM generate
    ranking and ordering queries.
    """

    @staticmethod
    def get_patterns() -> list[dict]:
        """
        Return ranking SQL patterns.
        """

        return RANKING_PATTERNS