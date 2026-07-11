class FewShotProvider:
    """
    Return the most relevant SQL examples
    according to the user's question.
    """

    def get_examples(
        self,
        question: str,
    ) -> str:

        question = question.lower()

        examples = []

        # ==================================================
        # COMMUNE
        # ==================================================

        if any(word in question for word in [

            "commune",
            "communes",

        ]):

            examples.append("""

Question:
Affiche toutes les communes.

SQL:
SELECT *
FROM COMMUNE;

----------------------------------------

Question:
Donne-moi les 10 premières communes.

SQL:
SELECT TOP (10)
    id_commune,
    nom_commune
FROM COMMUNE
ORDER BY nom_commune;

""")

        # ==================================================
        # REGION
        # ==================================================

        if any(word in question for word in [

            "région",
            "region",
            "régions",
            "regions",

        ]):

            examples.append("""

Question:
Prix moyen par région.

SQL:
SELECT
    r.nom_region,
    AVG(f.prix_moyen) AS prix_moyen
FROM FACT_PRIX_INDICES f
JOIN REGION r
ON f.id_region = r.id_region
GROUP BY r.nom_region;

""")

        # ==================================================
        # PRIX
        # ==================================================

        if any(word in question for word in [

            "prix",
            "indice",

        ]):

            examples.append("""

Question:
Prix moyen par année.

SQL:
SELECT
    annee,
    AVG(prix_moyen) AS prix_moyen
FROM FACT_PRIX_INDICES
GROUP BY annee
ORDER BY annee;

""")

        # ==================================================
        # LOYER
        # ==================================================

        if any(word in question for word in [

            "loyer",
            "loyers",

        ]):

            examples.append("""

Question:
Loyer moyen par quartier.

SQL:
SELECT
    q.nom_quartier,
    AVG(l.loyer_moyen_mad) AS loyer
FROM LOYER_QUARTIER l
JOIN QUARTIER q
ON l.id_quartier=q.id_quartier
GROUP BY q.nom_quartier;

""")

        # ==================================================
        # Aucun exemple trouvé
        # ==================================================

        if len(examples) == 0:

            examples.append("""

Question:
Combien existe-t-il de communes ?

SQL:
SELECT COUNT(*) AS nombre_communes
FROM COMMUNE;

""")

        return "\n".join(examples)