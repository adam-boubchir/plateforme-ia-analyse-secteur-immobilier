from app.dependencies.database import (
    get_immo_session,
)

from app.database.repositories.conversation_repository import (
    ConversationRepository,
)


def main():

    print("=" * 80)
    print("CONVERSATION REPOSITORY TEST")
    print("=" * 80)

    db = get_immo_session()

    repository = ConversationRepository(db)

    print()

    print(
        "Repository :",
        type(repository).__name__,
    )

    db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()