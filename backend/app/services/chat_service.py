from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)

from app.models.sql_agent_models import (
    SQLAgentResponse,
)

from app.services.conversation_service import (
    ConversationService,
)

from app.services.conversation_message_service import (
    ConversationMessageService,
)


class ChatService:
    """
    Main chat orchestrator.
    """

    def __init__(
        self,
        sql_agent: SQLAgent,
        conversation_service: ConversationService,
        message_service: ConversationMessageService,
    ):

        self.sql_agent = sql_agent

        self.conversation_service = conversation_service

        self.message_service = message_service

    def chat(
        self,
        question: str,
        conversation_uuid: str | None = None,
    ) -> SQLAgentResponse:
        """
        Process one chat message.
        """

        if conversation_uuid is None:
            conversation = self.conversation_service.create(
                title="Nouvelle conversation"
            )
        else:

            conversation = self.conversation_service.get_by_uuid(
                conversation_uuid
            )

            if conversation is None:

                raise ValueError(
                    "Conversation not found."
                )

        self.message_service.add_user_message(

            conversation_id=conversation.id,

            content=question,

        )

        response = self.sql_agent.ask(
            question
        )

        self.message_service.add_assistant_message(

            conversation_id=conversation.id,

            content=response.answer,

            generated_sql=response.sql,

            rows_returned=len(response.rows),

            rows=response.rows,

        )

        self.conversation_service.update_last_message(
            conversation
        )

        if (
            conversation.title is None
            or conversation.title == "Nouvelle conversation"
        ):

            self.conversation_service.update_title(
                conversation,
                question.strip()[:60],
            )

        # On ajoute le conversation_uuid dans la réponse
        response.conversation_uuid = conversation.conversation_uuid

        return response