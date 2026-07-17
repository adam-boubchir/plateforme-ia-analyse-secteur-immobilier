"""
Central business knowledge used by the SQL Context Engine.

This module is the single source of truth describing the
business meaning of every table.

Every builder (Business, Join, Synonyms, Examples...)
reads this file.
"""

DATABASE_KNOWLEDGE = {

    # ==========================================================
    # FACT_PRIX_INDICES
    # ==========================================================

    "FACT_PRIX_INDICES": {

        "business_name": "Construction Material Prices",

        "description": (
            "Stores construction material prices and material indices."
        ),

        "used_for": [

            "construction",

            "material",

            "prix",

            "prix moyen",

            "indice",

            "acier",

            "ciment",

            "béton",

            "brique",

            "sable",

            "bois",

            "bitume",

            "marbre",

            "verre",

        ],

        "never_use_for": [

            "loyer",

            "caution",

            "honoraires",

            "marché locatif",

        ],

        "main_columns": [

            "annee",

            "prix_moyen",

            "indice",

            "id_region",

            "id_province",

            "id_niveau_mat",

        ],

        "joins": [

            {

                "source_column": "id_region",

                "target_table": "REGION",

                "target_column": "id_region",

            },

            {

                "source_column": "id_province",

                "target_table": "PROVINCE_PREFECTURE",

                "target_column": "id_province",

            },

            {

                "source_column": "id_niveau_mat",

                "target_table": "NIVEAU_MATERIAU",

                "target_column": "id",

            },

        ],

        "forbidden_tables": [

            "FACT_INDICATEUR_HABITAT",

            "LOYER_QUARTIER",

        ],

    },

    # ==========================================================
    # FACT_INDICATEUR_HABITAT
    # ==========================================================

    "FACT_INDICATEUR_HABITAT": {

        "business_name": "Rental Market Indicators",

        "description": (
            "Stores rents, cautions and agency fees."
        ),

        "used_for": [

            "loyer",

            "caution",

            "honoraires",

            "marché locatif",

            "location",

        ],

        "never_use_for": [

            "acier",

            "ciment",

            "sable",

            "prix matériau",

        ],

        "main_columns": [

            "annee",

            "indice",

            "montant_mad",

            "id_region",

            "id_province",

            "id_type_habitat",

        ],

        "joins": [

            {

                "source_column": "id_region",

                "target_table": "REGION",

                "target_column": "id_region",

            },

            {

                "source_column": "id_province",

                "target_table": "PROVINCE_PREFECTURE",

                "target_column": "id_province",

            },

            {

                "source_column": "id_type_habitat",

                "target_table": "TYPE_HABITAT",

                "target_column": "id_type_habitat",

            },

            {

                "source_column": "id_envergure",

                "target_table": "ENVERGURE_HABITAT",

                "target_column": "id_envergure",

            },

        ],

        "forbidden_tables": [

            "NIVEAU_MATERIAU",

            "FACT_PRIX_INDICES",

        ],

    },

    # ==========================================================
    # REGION
    # ==========================================================

    "REGION": {

        "business_name": "Moroccan Regions",

        "description": (
            "Reference table containing Moroccan regions."
        ),

        "used_for": [

            "region",

            "territory",

        ],

        "never_use_for": [],

        "main_columns": [

            "id_region",

            "nom_region",

        ],

        "joins": [],

        "forbidden_tables": [],

    },

    # ==========================================================
    # PROVINCE_PREFECTURE
    # ==========================================================

    "PROVINCE_PREFECTURE": {

        "business_name": "Moroccan Provinces",

        "description": (
            "Reference table containing provinces and prefectures."
        ),

        "used_for": [

            "province",

            "préfecture",

        ],

        "never_use_for": [],

        "main_columns": [

            "id_province",

            "nom_province",

        ],

        "joins": [],

        "forbidden_tables": [],

    },

    # ==========================================================
    # TYPE_HABITAT
    # ==========================================================

    "TYPE_HABITAT": {

        "business_name": "Housing Types",

        "description": (
            "Reference table containing housing categories."
        ),

        "used_for": [

            "villa",

            "appartement",

            "habitat",

        ],

        "never_use_for": [],

        "main_columns": [

            "id_type_habitat",

            "nom_type",

        ],

        "joins": [],

        "forbidden_tables": [],

    },

}