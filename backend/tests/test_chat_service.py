from app.dependencies.database import (
    get_immo_session,
)

from app.dependencies.sql_agent import (
    get_sql_agent,
)

from app.services.conversation_service import (
    ConversationService,
)

from app.services.conversation_message_service import (
    ConversationMessageService,
)

from app.services.chat_service import (
    ChatService,
)


def main():

    print("=" * 80)
    print("CHAT SERVICE TEST")
    print("=" * 80)

    db = get_immo_session()

    sql_agent = get_sql_agent(db)

    conversation_service = ConversationService(db)

    message_service = ConversationMessageService(db)

    chat_service = ChatService(

        sql_agent=sql_agent,

        conversation_service=conversation_service,

        message_service=message_service,

    )

    response = chat_service.chat(

        question="Liste toutes les régions"

    )

    print()

    print("=" * 80)
    print("CHAT RESPONSE")
    print("=" * 80)

    print()

    print("Success :", response.success)

    print()

    print("Answer :")

    print(response.answer)

    print()

    print("SQL :")

    print(response.sql)

    print()

    print("Rows :", len(response.rows))

    print()

    print("✅ TEST PASSED")

    db.close()


if __name__ == "__main__":
    main()