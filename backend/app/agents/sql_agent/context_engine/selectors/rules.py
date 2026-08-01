from __future__ import annotations

from dataclasses import dataclass, field

__all__ = [
    "Rule",
    "RULES",
]


@dataclass(slots=True)
class Rule:
    """
    Represents a business rule used by the KnowledgeSelector.

    A rule defines:
    - keywords that activate it;
    - related database tables;
    - business metadata;
    - SQL generation hints.
    """

    name: str

    keywords: list[str] = field(default_factory=list)

    tables: list[str] = field(default_factory=list)

    business_domain: str | None = None

    question_type: str | None = None

    sql_pattern: str | None = None

    needs_join: bool = False

    aggregation: bool = False

    geographic: bool = False

    time_series: bool = False


# ==========================================================
# BUSINESS RULES
# ==========================================================

RULES: list[Rule] = [

    # ======================================================
    # CONSTRUCTION MATERIALS
    # ======================================================

    Rule(
        name="Construction Materials",
        keywords=[
            "ciment",
            "acier",
            "fer",
            "béton",
            "beton",
            "brique",
            "sable",
            "gravier",
            "bois",
            "matériau",
            "materiau",
        ],
        tables=[
            "FACT_PRIX_INDICES",
            "NIVEAU_MATERIAU",
            "REGION",
            "PROVINCE_PREFECTURE",
        ],
        business_domain="Construction Materials",
        needs_join=True,
    ),

    # ======================================================
    # HOUSING
    # ======================================================

    Rule(
        name="Housing",
        keywords=[
            "loyer",
            "loyers",
            "location",
            "villa",
            "appartement",
            "habitat",
            "logement",
            "caution",
            "honoraire",
        ],
        tables=[
            "FACT_INDICATEUR_HABITAT",
            "TYPE_HABITAT",
            "REGION",
            "PROVINCE_PREFECTURE",
            "COMMUNE",
        ],
        business_domain="Rental Market",
        needs_join=True,
    ),

    # ======================================================
    # AVERAGE
    # ======================================================

    Rule(
        name="Average",
        keywords=[
            "moyenne",
            "moyen",
            "average",
            "avg",
        ],
        question_type="Average",
        sql_pattern="Aggregate",
        aggregation=True,
    ),

    # ======================================================
    # RANKING
    # ======================================================

    Rule(
        name="Ranking",
        keywords=[
            "top",
            "classement",
            "plus cher",
            "plus chers",
            "maximum",
            "minimum",
            "meilleur",
            "plus élevé",
            "plus bas",
        ],
        question_type="Ranking",
        sql_pattern="Ranking",
    ),

    # ======================================================
    # COMPARISON
    # ======================================================

    Rule(
        name="Comparison",
        keywords=[
            "compare",
            "comparer",
            "comparaison",
            "vs",
            "versus",
            "différence",
            "difference",
        ],
        question_type="Comparison",
        sql_pattern="Comparison",
        aggregation=True,
    ),

    # ======================================================
    # EVOLUTION
    # ======================================================

    Rule(
        name="Evolution",
        keywords=[
            "évolution",
            "evolution",
            "historique",
            "tendance",
            "progression",
        ],
        question_type="Evolution",
        sql_pattern="Evolution",
        aggregation=True,
        time_series=True,
    ),

    # ======================================================
    # GEOGRAPHIC
    # ======================================================

    Rule(
        name="Geographic",
        keywords=[
            "région",
            "region",
            "province",
            "préfecture",
            "prefecture",
            "commune",
            "ville",
        ],
        tables=[
            "REGION",
            "PROVINCE_PREFECTURE",
            "COMMUNE",
        ],
        geographic=True,
        needs_join=True,
    ),
]