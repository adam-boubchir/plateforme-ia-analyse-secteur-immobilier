from app.dependencies.database import (
    get_immo_session,
)

from app.services.conversation_service import (
    ConversationService,
)

from app.services.conversation_message_service import (
    ConversationMessageService,
)


def main():

    print("=" * 80)
    print("CONVERSATION MESSAGE SERVICE TEST")
    print("=" * 80)

    db = get_immo_session()

    conversation_service = ConversationService(db)

    message_service = ConversationMessageService(db)

    conversation = conversation_service.create(
        title="Test Conversation"
    )

    message_service.add_user_message(

        conversation_id=conversation.id,

        content="Quel est le prix moyen à Rabat ?"

    )

    message_service.add_assistant_message(

        conversation_id=conversation.id,

        content="Le prix moyen est de 12 000 MAD.",

        generated_sql="SELECT ...",

        rows_returned=1,

        execution_time_ms=120,

    )

    messages = message_service.get_messages(
        conversation.id
    )

    print()

    print("Conversation :", conversation.id)

    print("Messages :", len(messages))

    print(
        "Count :",
        message_service.count_messages(
            conversation.id
        )
    )

    print()

    for message in messages:

        print(
            message.role,
            "->",
            message.content,
        )

    print()

    print("✅ TEST PASSED")

    db.close()


if __name__ == "__main__":
    main()