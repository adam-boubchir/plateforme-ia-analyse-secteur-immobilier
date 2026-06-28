from app.database.session import get_immo_db
from app.services.metadata_service import MetadataService


def main():

    db = next(get_immo_db())

    try:

        print("=" * 80)
        print("METADATA SERVICE TEST")
        print("=" * 80)

        service = MetadataService(db)

        # Tables
        tables = service.get_tables()

        print(f"\nTables : {len(tables)}")

        # Table spécifique
        table = service.get_table(
            "dbo",
            "FACT_PRIX_INDICES"
        )

        if table:
            print(f"Table trouvée : {table.table_name}")
        else:
            print("Table non trouvée")

        # Colonnes
        columns = service.get_columns(
            "FACT_PRIX_INDICES"
        )

        print(f"Colonnes : {len(columns)}")

        # Relations
        relationships = service.get_relationships()

        print(f"Relations : {len(relationships)}")

        print("\n===== SAMPLE TABLES =====")

        for table in tables[:5]:
            print(
                f"{table.schema_name}.{table.table_name}"
            )

        print("\n===== SAMPLE COLUMNS =====")

        for column in columns[:5]:
            print(
                f"{column.column_name} ({column.data_type})"
            )

        print("\n===== SAMPLE RELATIONSHIPS =====")

        for relation in relationships[:5]:
            print(
                f"{relation.source_table}.{relation.source_column}"
                f" -> "
                f"{relation.target_table}.{relation.target_column}"
            )

        print("\n✅ TEST PASSED")

    finally:

        db.close()


if __name__ == "__main__":
    main()