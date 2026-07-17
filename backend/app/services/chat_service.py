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
    Main orchestration service of the AI platform.

    Responsibilities
    ----------------
    • Manage conversations
    • Store user messages
    • Delegate the question to the appropriate AI agent
    • Store assistant responses
    • Update conversation metadata
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

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def chat(
        self,
        question: str,
        conversation_uuid: str | None = None,
    ) -> SQLAgentResponse:
        """
        Process one user question.
        """

        conversation = self._get_or_create_conversation(
            conversation_uuid
        )

        # ------------------------------------------------------
        # Store user message
        # ------------------------------------------------------

        self.message_service.add_user_message(

            conversation_id=conversation.id,

            content=question,

        )

        # ------------------------------------------------------
        # SQL Agent
        # ------------------------------------------------------

        response = self.sql_agent.ask(

            question=question,

            conversation_id=conversation.id,

        )

        # ------------------------------------------------------
        # Store assistant message
        # ------------------------------------------------------

        self.message_service.add_assistant_message(

            conversation_id=conversation.id,

            content=response.answer,

            generated_sql=response.sql,

            rows_returned=len(response.rows),

            rows=response.rows,

        )

        # ------------------------------------------------------
        # Update conversation metadata
        # ------------------------------------------------------

        self.conversation_service.update_last_message(
            conversation
        )

        self._update_title_if_needed(

            conversation,

            question,

        )

        response.conversation_uuid = (
            conversation.conversation_uuid
        )

        return response

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_or_create_conversation(
        self,
        conversation_uuid: str | None,
    ):
        """
        Retrieve or create a conversation.
        """

        if conversation_uuid is None:

            return self.conversation_service.create(

                title="Nouvelle conversation"

            )

        conversation = self.conversation_service.get_by_uuid(

            conversation_uuid

        )

        if conversation is None:

            raise ValueError(
                "Conversation not found."
            )

        return conversation

    def _update_title_if_needed(
        self,
        conversation,
        question: str,
    ) -> None:
        """
        Automatically generate the title of a new conversation.
        """

        if (

            conversation.title is None

            or conversation.title == "Nouvelle conversation"

        ):

            self.conversation_service.update_title(

                conversation,

                question.strip()[:60],

            )