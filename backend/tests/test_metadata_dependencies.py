from app.dependencies.database import (
    get_immo_session,
)

from app.dependencies.metadata import (
    get_metadata_service,
    get_sql_context_builder,
)


def main():

    print("=" * 80)
    print("METADATA DEPENDENCIES TEST")
    print("=" * 80)

    db = get_immo_session()

    metadata_service = get_metadata_service(db)

    context_builder = get_sql_context_builder(db)

    print()

    print(
        "MetadataService :",
        type(metadata_service).__name__,
    )

    print(
        "SQLContextBuilder :",
        type(context_builder).__name__,
    )

    db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()