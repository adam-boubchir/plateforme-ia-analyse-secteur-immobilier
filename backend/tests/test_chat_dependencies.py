from app.dependencies.database import (
    get_immo_session,
)

from app.dependencies.chat import (
    get_chat_service,
)


def main():

    print("=" * 80)
    print("CHAT DEPENDENCIES TEST")
    print("=" * 80)

    db = get_immo_session()

    chat_service = get_chat_service(db)

    print()

    print(
        "ChatService :",
        type(chat_service).__name__,
    )

    print()

    print("✅ TEST PASSED")

    db.close()


if __name__ == "__main__":
    main()