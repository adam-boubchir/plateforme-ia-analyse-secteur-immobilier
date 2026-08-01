# ==========================================================
# CONSTANTS
# ==========================================================

COMPARISON_PATTERNS = [
    {
        "name": "Compare Two Values",
        "category": "Comparison",
        "intent": [
            "compare",
            "comparison",
            "versus",
            "vs",
            "difference",
            "différence",
            "comparer",
        ],
        "description": (
            "Compare two entities using the same metric."
        ),
        "functions": [
            "WHERE",
            "IN",
            "GROUP BY",
        ],
        "keywords": [
            "IN",
            "GROUP BY",
        ],
        "template": """
SELECT
    entity,
    AVG(metric)
FROM table_name
WHERE entity IN ('A','B')
GROUP BY entity;
""".strip(),
        "recommendation": (
            "Use GROUP BY to compare entities."
        ),
    },
    {
        "name": "Compare Regions",
        "category": "Comparison",
        "intent": [
            "region",
            "région",
            "province",
            "ville",
            "agglomération",
        ],
        "description": (
            "Compare geographic areas."
        ),
        "functions": [
            "JOIN",
            "GROUP BY",
        ],
        "keywords": [
            "REGION",
            "PROVINCE",
            "GROUP BY",
        ],
        "template": """
SELECT
    r.nom_region,
    AVG(f.metric)
FROM FACT_TABLE f
INNER JOIN REGION r
    ON f.id_region = r.id_region
GROUP BY
    r.nom_region;
""".strip(),
        "recommendation": (
            "Always join the geographic dimension."
        ),
    },
    {
        "name": "Compare Years",
        "category": "Comparison",
        "intent": [
            "year",
            "année",
            "entre",
            "2021",
            "2022",
            "2023",
        ],
        "description": (
            "Compare values across years."
        ),
        "functions": [
            "GROUP BY",
            "ORDER BY",
        ],
        "keywords": [
            "annee",
            "GROUP BY",
        ],
        "template": """
SELECT
    annee,
    AVG(metric)
FROM FACT_TABLE
GROUP BY
    annee
ORDER BY
    annee;
""".strip(),
        "recommendation": (
            "Sort results chronologically."
        ),
    },
    {
        "name": "Compare Categories",
        "category": "Comparison",
        "intent": [
            "type",
            "catégorie",
            "catégorie habitat",
            "matériau",
            "produit",
        ],
        "description": (
            "Compare business categories."
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
    AVG(metric)
FROM FACT_TABLE
GROUP BY
    category;
""".strip(),
        "recommendation": (
            "Aggregate by category."
        ),
    },
]


class ComparisonPatterns:
    """
    Collection of SQL comparison patterns.

    These patterns help the LLM generate SQL
    queries comparing two or more entities.
    """

    @staticmethod
    def get_patterns() -> list[dict]:
        """
        Return comparison SQL patterns.
        """

        return COMPARISON_PATTERNS