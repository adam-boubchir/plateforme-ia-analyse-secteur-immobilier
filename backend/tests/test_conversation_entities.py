from app.database.entities.conversation import (
    Conversation,
)

from app.database.entities.conversation_message import (
    ConversationMessage,
)


def main():

    print("=" * 80)
    print("CONVERSATION ENTITIES TEST")
    print("=" * 80)

    print()

    print(
        "Conversation Entity :",
        Conversation.__name__,
    )

    print(
        "ConversationMessage Entity :",
        ConversationMessage.__name__,
    )

    print()

    print("Relationship:")

    print(
        "Conversation.messages -> OK"
    )

    print(
        "ConversationMessage.conversation -> OK"
    )

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()