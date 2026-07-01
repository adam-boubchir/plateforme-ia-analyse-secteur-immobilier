from app.dependencies.database import (
    get_immo_session,
)

from app.services.conversation_service import (
    ConversationService,
)


def main():

    print("=" * 80)
    print("SAVE EXCHANGE TEST")
    print("=" * 80)

    db = get_immo_session()

    service = ConversationService(db)

    exchange = service.save_exchange(

        question="Quel est le prix moyen à Rabat ?",

        answer="Le prix moyen est de 12 000 MAD.",

    )

    print()

    print("Conversation ID :", exchange.conversation_id)

    print("Request ID      :", exchange.request_id)

    print("Question        :", exchange.user_message)

    print("Réponse         :", exchange.assistant_response)

    print("Status          :", exchange.status)

    print()

    print("✅ TEST PASSED")

    db.close()


if __name__ == "__main__":
    main()