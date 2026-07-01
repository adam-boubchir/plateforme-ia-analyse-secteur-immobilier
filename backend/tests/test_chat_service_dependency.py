from app.dependencies.database import (
    get_ministry_session,
)

from app.dependencies.chat_service import (
    get_chat_service,
)


def main():

    print("=" * 80)
    print("CHAT SERVICE DEPENDENCY TEST")
    print("=" * 80)

    db = get_ministry_session()

    service = get_chat_service(db)

    print()

    print(
        "ChatService :",
        type(service).__name__,
    )

    db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()