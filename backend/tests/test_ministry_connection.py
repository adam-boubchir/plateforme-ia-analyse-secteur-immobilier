from __future__ import annotations

from sqlalchemy import text

from app.database.connection_ministry import (
    engine_ministry,
)


def main() -> None:

    print()
    print("=" * 80)
    print("MINISTRY DATABASE CONNECTION TEST")
    print("=" * 80)

    with engine_ministry.connect() as connection:

        # ======================================================
        # DATABASE INFORMATION
        # ======================================================

        database_name = connection.execute(
            text("SELECT DB_NAME()")
        ).scalar()

        schema_name = connection.execute(
            text("SELECT SCHEMA_NAME()")
        ).scalar()

        print()
        print("Database :", database_name)
        print("Schema   :", schema_name)

        # ======================================================
        # TEST NIVEAU_MATERIAU
        # ======================================================

        print()
        print("-" * 80)
        print("TEST NIVEAU_MATERIAU")
        print("-" * 80)

        result = connection.execute(
            text(
                """
                SELECT
                    f.id_niveau_mat,
                    nm.nom,
                    nm.niveau,
                    COUNT(*) AS nombre_lignes,
                    COUNT(f.prix_moyen) AS nombre_prix,
                    COUNT(f.indice) AS nombre_indices,
                    MIN(f.annee) AS premiere_annee,
                    MAX(f.annee) AS derniere_annee
                FROM dbo.FACT_PRIX_INDICES f
                INNER JOIN dbo.NIVEAU_MATERIAU nm
                    ON f.id_niveau_mat = nm.id
                GROUP BY
                    f.id_niveau_mat,
                    nm.nom,
                    nm.niveau
                HAVING nm.nom LIKE '%Ciment%'
                ORDER BY f.id_niveau_mat
                """
            )
        )

        rows = result.mappings().all()

        print()
        print("-" * 80)
        print("MATERIAUX CIMENT REELLEMENT PRESENTS DANS FACT_PRIX_INDICES")
        print("-" * 80)

        for row in rows:
            print(dict(row))

        print(f"\nNombre de résultats : {len(rows)}")


if __name__ == "__main__":
    main()