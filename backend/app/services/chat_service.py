from app.agents.orchestrator.orchestrator_service import (
    OrchestratorService,
)
from app.database.entities.conversation import (
    Conversation,
)
from app.models.agent_response import (
    AgentResponse,
)
from app.services.conversation_message_service import (
    ConversationMessageService,
)
from app.services.conversation_service import (
    ConversationService,
)


class ChatService:
    """
    Main orchestration service of the AI platform.

    Responsibilities
    ----------------
    • Manage conversations
    • Store user messages
    • Delegate requests to the Orchestrator
    • Store assistant responses
    • Update conversation metadata
    """

    DEFAULT_CONVERSATION_TITLE = "Nouvelle conversation"

    def __init__(
        self,
        orchestrator_service: OrchestratorService,
        conversation_service: ConversationService,
        message_service: ConversationMessageService,
    ) -> None:

        self.orchestrator_service: OrchestratorService = (
            orchestrator_service
        )

        self.conversation_service: ConversationService = (
            conversation_service
        )

        self.message_service: ConversationMessageService = (
            message_service
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def chat(
        self,
        question: str,
        conversation_uuid: str | None = None,
    ) -> AgentResponse:
        """
        Process a user request.
        """

        conversation: Conversation = (
            self._get_or_create_conversation(
                conversation_uuid=conversation_uuid,
            )
        )

        self.message_service.add_user_message(
            conversation_id=conversation.id,
            content=question,
        )

        response: AgentResponse = (
            self.orchestrator_service.route(
                question=question,
                conversation_id=conversation.id,
            )
        )

        self.message_service.add_assistant_message(
            conversation_id=conversation.id,
            content=response.answer,
            generated_sql=response.sql,
            rows_returned=len(response.rows),
            rows=response.rows,
        )

        self.conversation_service.update_last_message(
            conversation=conversation,
        )

        self._update_title_if_needed(
            conversation=conversation,
            question=question,
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
    ) -> Conversation:
        """
        Retrieve an existing conversation or create a new one.
        """

        if conversation_uuid is None:
            return self.conversation_service.create(
                title=self.DEFAULT_CONVERSATION_TITLE,
            )

        conversation = self.conversation_service.get_by_uuid(
            conversation_uuid=conversation_uuid,
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        return conversation

    def _update_title_if_needed(
        self,
        conversation: Conversation,
        question: str,
    ) -> None:
        """
        Automatically set the conversation title
        from the first user message.
        """

        if (
            conversation.title is None
            or conversation.title == self.DEFAULT_CONVERSATION_TITLE
        ):
            self.conversation_service.update_title(
                conversation=conversation,
                title=question.strip()[:60],
            )


__all__ = [
    "ChatService",
]