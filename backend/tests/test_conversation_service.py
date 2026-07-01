from app.dependencies.database import (
    get_immo_session,
)

from app.services.conversation_service import (
    ConversationService,
)


def main():

    print("=" * 80)
    print("CONVERSATION SERVICE TEST")
    print("=" * 80)

    db = get_immo_session()

    service = ConversationService(
        db
    )

    conversation = service.create()

    print()

    print(
        "ID:",
        conversation.id,
    )

    print(
        "UUID:",
        conversation.conversation_uuid,
    )

    print(
        "Status:",
        conversation.status,
    )

    print()

    print("Total conversations :")

    print(
        len(
            service.get_all()
        )
    )

    print()

    print("✅ TEST PASSED")

    db.close()


if __name__ == "__main__":
    main()