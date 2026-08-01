"""
Central repository of SQL Agent few-shot examples.

Each example contains:

- question
- sql
- keywords

The FewShotProvider automatically selects the most
relevant examples according to the user question.

Later this file can easily be replaced by
vector search (embeddings / RAG).
"""

FEW_SHOT_EXAMPLES = [

    # ==========================================================
    # AVERAGE
    # ==========================================================

    {
        "question": "Quel est le prix moyen du ciment ?",

        "keywords": [
            "moyenne",
            "prix moyen",
            "average",
            "ciment",
        ],

        "sql": """
SELECT
    AVG(f.Valeur) AS PrixMoyen
FROM FACT_PRIX_INDICES f
INNER JOIN NIVEAU_MATERIAU m
INNER JOIN NIVEAU_MATERIAU m
    ON f.IdNiveauMateriau = m.IdNiveauMateriau
WHERE m.Libelle = 'Ciment'
""".strip(),
    },

    # ==========================================================
    # REGION
    # ==========================================================

    {
        "question": "Prix moyen du ciment à Casablanca",

        "keywords": [
            "casablanca",
            "région",
            "prix",
            "ciment",
        ],

        "sql": """
SELECT
    r.LibelleRegion,
    AVG(f.Valeur) AS PrixMoyen
FROM FACT_PRIX_INDICES f
INNER JOIN REGION r
ON f.IdRegion = r.IdRegion
INNER JOIN NIVEAU_MATERIAU m
ON f.IdNiveauMateriau = m.IdNiveauMateriau
WHERE
    r.LibelleRegion = 'Casablanca-Settat'
    AND m.Libelle = 'Ciment'
GROUP BY 
    r.LibelleRegion
""".strip(),
    },

    # ==========================================================
    # RANKING
    # ==========================================================

    {
        "question": "Top 10 des régions les plus chères",

        "keywords": [
            "top",
            "plus cher",
            "classement",
            "ranking",
        ],

        "sql": """
SELECT TOP 10

    r.LibelleRegion,

    AVG(f.Valeur) AS PrixMoyen

FROM FACT_PRIX_INDICES f

INNER JOIN REGION r

ON f.IdRegion = r.IdRegion

GROUP BY r.LibelleRegion

ORDER BY 
    PrixMoyen DESC
""".strip(),
    },

    # ==========================================================
    # EVOLUTION
    # ==========================================================

    {
        "question": "Evolution du prix du ciment",

        "keywords": [
            "évolution",
            "historique",
            "tendance",
            "année",
        ],

        "sql": """
SELECT

    f.Annee,

    AVG(f.Valeur) AS PrixMoyen

FROM FACT_PRIX_INDICES f

INNER JOIN NIVEAU_MATERIAU m

ON f.IdNiveauMateriau=m.IdNiveauMateriau

WHERE 
    m.Libelle = 'Ciment'

GROUP BY f.Annee

ORDER BY f.Annee
""".strip(),
    },

    # ==========================================================
    # COUNT
    # ==========================================================

    {
        "question": "Combien de logements existent ?",

        "keywords": [
            "combien",
            "nombre",
            "count",
            "logement",
        ],

        "sql": """
SELECT

COUNT(*) AS NombreLogements

FROM FACT_INDICATEUR_HABITAT f
""".strip(),
    },

    # ==========================================================
    # MAX
    # ==========================================================

    {
        "question": "Quel est le prix maximum ?",

        "keywords": [
            "maximum",
            "max",
            "plus élevé",
        ],

        "sql": """
SELECT

    MAX(f.Valeur) AS PrixMaximum

FROM FACT_PRIX_INDICES f
""".strip(),
    },

    # ==========================================================
    # MIN
    # ==========================================================

    {
        "question": "Quel est le prix minimum ?",

        "keywords": [
            "minimum",
            "min",
            "plus faible",
        ],

        "sql": """
SELECT

MIN(f.Valeur) AS PrixMinimum

FROM FACT_PRIX_INDICES f
""".strip(),
    },

]