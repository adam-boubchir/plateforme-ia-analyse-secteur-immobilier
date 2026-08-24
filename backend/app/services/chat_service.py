from __future__ import annotations

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

__all__ = (
    "ChatService",
)

# ==========================================================
# CONSTANTS
# ==========================================================

_DEFAULT_CONVERSATION_TITLE = "Nouvelle conversation"
_MAX_TITLE_LENGTH = 60


class ChatService:
    """
    Main orchestration service of the AI platform.

    Responsibilities:
        - Manage conversations.
        - Persist user messages.
        - Persist assistant messages.
        - Delegate requests to the AI orchestrator.
        - Maintain conversation metadata.

    This service intentionally contains no AI business logic.
    """

    def __init__(
        self,
        *,
        orchestrator_service: OrchestratorService,
        conversation_service: ConversationService,
        message_service: ConversationMessageService,
    ) -> None:
        """
        Initialize the chat service.

        Args:
            orchestrator_service:
                Service responsible for routing AI requests.

            conversation_service:
                Conversation management service.

            message_service:
                Conversation message service.
        """

        self._orchestrator_service = orchestrator_service
        self._conversation_service = conversation_service
        self._message_service = message_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def chat(
        self,
        *,
        question: str,
        conversation_uuid: str | None = None,
    ) -> AgentResponse:
        """
        Process a user request through the AI platform.

        Args:
            question:
                User question.

            conversation_uuid:
                Existing conversation identifier.

        Returns:
            Agent response enriched with the conversation UUID.
        """

        conversation = self._get_or_create_conversation(
            conversation_uuid=conversation_uuid,
        )

        self._store_user_message(
            conversation_id=conversation.id,
            question=question,
        )

        response = self._orchestrator_service.route(
            question=question,
            conversation_id=conversation.id,
        )

        self._store_assistant_message(
            conversation_id=conversation.id,
            response=response,
        )

        self._finalize_conversation(
            conversation=conversation,
            question=question,
        )

        response.conversation_uuid = (
            conversation.conversation_uuid
        )

        final_response = response

        return final_response

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_or_create_conversation(
        self,
        *,
        conversation_uuid: str | None,
    ) -> Conversation:
        """
        Retrieve an existing conversation or create a new one.

        Args:
            conversation_uuid:
                Conversation identifier.

        Returns:
            Existing or newly created conversation.

        Raises:
            ValueError:
                If the conversation does not exist.
        """

        if conversation_uuid is None:
            conversation = self._conversation_service.create(
                title=_DEFAULT_CONVERSATION_TITLE,
            )

            return conversation

        conversation = self._conversation_service.get_by_uuid(
            conversation_uuid=conversation_uuid,
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found.",
            )

        return conversation

    def _store_user_message(
        self,
        *,
        conversation_id: int,
        question: str,
    ) -> None:
        """
        Persist the user message.

        Args:
            conversation_id:
                Conversation identifier.

            question:
                User question.
        """

        self._message_service.add_user_message(
            conversation_id=conversation_id,
            content=question,
        )

    def _store_assistant_message(
        self,
        *,
        conversation_id: int,
        response: AgentResponse,
    ) -> None:
        """
        Persist the assistant response.

        Args:
            conversation_id:
                Conversation identifier.

            response:
                AI response.
        """

        rows_returned = len(
            response.rows,
        )

        self._message_service.add_assistant_message(
            conversation_id=conversation_id,
            content=response.answer,
            generated_sql=response.sql,
            rows_returned=rows_returned,
            rows=response.rows,
            pdf_path=getattr(
                response,
                "pdf_path",
                None,
            ),
        )

    def _finalize_conversation(
        self,
        *,
        conversation: Conversation,
        question: str,
    ) -> None:
        """
        Update conversation metadata.

        Args:
            conversation:
                Conversation entity.

            question:
                User question.
        """

        self._conversation_service.update_last_message(
            conversation=conversation,
        )

        self._update_title_if_needed(
            conversation=conversation,
            question=question,
        )

    def _update_title_if_needed(
        self,
        *,
        conversation: Conversation,
        question: str,
    ) -> None:
        """
        Update the conversation title using the first user question.

        Args:
            conversation:
                Conversation entity.

            question:
                User question.
        """

        if (
            conversation.title is None
            or conversation.title == _DEFAULT_CONVERSATION_TITLE
        ):
            title = question.strip()[
                :_MAX_TITLE_LENGTH
            ]

            self._conversation_service.update_title(
                conversation=conversation,
                title=title,
            )

    def get_conversation(
        self,
        *,
        conversation_uuid: str,
    ) -> Conversation:
        """
        Return an existing conversation.
        """

        conversation = self._conversation_service.get_by_uuid(
            conversation_uuid=conversation_uuid,
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found.",
            )

        return conversation