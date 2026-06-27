from app.audit.database_auditor import DatabaseAuditor

from app.database.session import (
    get_immo_db,
    get_ministry_db,
)

from app.metadata.metadata_loader import MetadataLoader

from app.database.entities.table_metadata import TableMetadataEntity
from app.database.entities.column_metadata import ColumnMetadataEntity
from app.database.entities.relationship import RelationshipEntity


def main():

    ministry_db = next(get_ministry_db())

    immo_db = next(get_immo_db())

    try:

        print("=" * 80)
        print("METADATA LOADER TEST")
        print("=" * 80)

        print("\n1. Running DatabaseAuditor...")

        auditor = DatabaseAuditor(ministry_db)

        report = auditor.build_report()

        print("✓ Audit completed.")

        print("\n2. Loading metadata into IMMO_AI...")

        loader = MetadataLoader(immo_db)

        loader.load(report)

        print("✓ Metadata loaded.")

        print("\n3. Verification")

        table_count = (
            immo_db.query(TableMetadataEntity)
            .count()
        )

        column_count = (
            immo_db.query(ColumnMetadataEntity)
            .count()
        )

        relationship_count = (
            immo_db.query(RelationshipEntity)
            .count()
        )

        print("-" * 40)

        print(f"Tables         : {table_count}")

        print(f"Columns        : {column_count}")

        print(f"Relationships  : {relationship_count}")

        print("\n✓ TEST PASSED")

    finally:

        ministry_db.close()

        immo_db.close()


if __name__ == "__main__":
    main()