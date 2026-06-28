from app.database.session import get_immo_db
from app.services.metadata_service import MetadataService
from app.agents.sql_agent.sql_context_builder import SQLContextBuilder


def main():

    db = next(get_immo_db())

    try:

        print("=" * 80)
        print("SQL CONTEXT BUILDER TEST")
        print("=" * 80)

        # Metadata service
        metadata_service = MetadataService(db)

        # Context builder
        context_builder = SQLContextBuilder(
            metadata_service
        )

        # Build context
        context = context_builder.build_context()

        print("\nGenerated Context\n")
        print("=" * 80)
        print(context)
        print("=" * 80)

        print("\nContext length :", len(context))

        print("\n✓ TEST PASSED")

    finally:

        db.close()


if __name__ == "__main__":
    main()