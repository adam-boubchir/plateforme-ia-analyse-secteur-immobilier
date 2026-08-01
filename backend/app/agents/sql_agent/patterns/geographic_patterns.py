# ==========================================================
# CONSTANTS
# ==========================================================

GEOGRAPHIC_PATTERNS = [
    {
        "name": "Filter By Region",
        "category": "Geographic",
        "intent": [
            "region",
            "région",
            "par région",
        ],
        "description": (
            "Filter data using the REGION dimension."
        ),
        "functions": [
            "JOIN",
            "WHERE",
        ],
        "keywords": [
            "REGION",
            "JOIN",
        ],
        "template": """
SELECT
    r.nom_region,
    AVG(metric)
FROM FACT_TABLE f
INNER JOIN REGION r
    ON f.id_region = r.id_region
WHERE
    r.nom_region = 'Rabat-Salé-Kénitra'
GROUP BY
    r.nom_region;
""".strip(),
        "recommendation": (
            "Always join the REGION table before filtering."
        ),
    },
    {
        "name": "Filter By Province",
        "category": "Geographic",
        "intent": [
            "province",
            "préfecture",
        ],
        "description": (
            "Filter data using provinces."
        ),
        "functions": [
            "JOIN",
            "WHERE",
        ],
        "keywords": [
            "PROVINCE",
        ],
        "template": """
SELECT
    p.nom_province,
    AVG(metric)
FROM FACT_TABLE f
INNER JOIN PROVINCE_PREFECTURE p
    ON f.id_province = p.id_province
WHERE
    p.nom_province = 'Rabat'
GROUP BY
    p.nom_province;
""".strip(),
        "recommendation": (
            "Join the province table before filtering."
        ),
    },
    {
        "name": "Compare Regions",
        "category": "Geographic",
        "intent": [
            "compare regions",
            "comparer régions",
            "différence région",
        ],
        "description": (
            "Compare several geographic regions."
        ),
        "functions": [
            "GROUP BY",
            "JOIN",
        ],
        "keywords": [
            "GROUP BY",
        ],
        "template": """
SELECT
    r.nom_region,
    AVG(metric)
FROM FACT_TABLE f
INNER JOIN REGION r
    ON f.id_region = r.id_region
GROUP BY
    r.nom_region;
""".strip(),
        "recommendation": (
            "Group by geographic entity."
        ),
    },
    {
        "name": "Geographic Ranking",
        "category": "Geographic",
        "intent": [
            "top régions",
            "meilleures régions",
            "classement régions",
        ],
        "description": (
            "Rank geographic entities."
        ),
        "functions": [
            "TOP",
            "ORDER BY",
            "GROUP BY",
        ],
        "keywords": [
            "TOP",
            "DESC",
        ],
        "template": """
SELECT TOP (10)
    r.nom_region,
    AVG(metric)
FROM FACT_TABLE f
INNER JOIN REGION r
    ON f.id_region = r.id_region
GROUP BY
    r.nom_region
ORDER BY
    AVG(metric) DESC;
""".strip(),
        "recommendation": (
            "Use TOP with ORDER BY DESC."
        ),
    },
    {
        "name": "Geographic Evolution",
        "category": "Geographic",
        "intent": [
            "évolution région",
            "tendance région",
        ],
        "description": (
            "Analyse the evolution by geographic area."
        ),
        "functions": [
            "GROUP BY",
            "ORDER BY",
        ],
        "keywords": [
            "GROUP BY",
            "ORDER BY",
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
    r.nom_region,
    annee;
""".strip(),
        "recommendation": (
            "Sort by region and year for better readability."
        ),
    },
]


class GeographicPatterns:
    """
    Collection of SQL geographic patterns.

    These patterns guide the LLM when answering
    geographic analysis questions.
    """

    @staticmethod
    def get_patterns() -> list[dict]:
        """
        Return geographic SQL patterns.
        """

        return GEOGRAPHIC_PATTERNS