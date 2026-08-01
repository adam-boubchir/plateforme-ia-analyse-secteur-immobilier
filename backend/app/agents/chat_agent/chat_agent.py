from __future__ import annotations

from app.agents.base.base_agent import BaseAgent
from app.agents.chat_agent.chat_generator import ChatGenerator
from app.agents.chat_agent.chat_prompt_builder import ChatPromptBuilder
from app.models.chat_agent_models import ChatAgentResponse

__all__ = ["ChatAgent"]


class ChatAgent(BaseAgent):
    """
    AI agent responsible for answering general conversational questions.

    Pipeline:
        User Question
            ↓
        Prompt Building
            ↓
        LLM Generation
            ↓
        Chat Response
    """

    def __init__(
        self,
        prompt_builder: ChatPromptBuilder,
        generator: ChatGenerator,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.generator = generator

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def ask(
        self,
        question: str,
        conversation_id: int,
    ) -> ChatAgentResponse:
        """
        Generate a conversational response.

        Args:
            question: User question.
            conversation_id: Conversation identifier (reserved for future use).

        Returns:
            ChatAgentResponse containing the generated answer.
        """

        prompt = self.prompt_builder.build_prompt(
            question=question,
        )

        answer = self.generator.generate(
            prompt,
        )

        return ChatAgentResponse(
            success=True,
            answer=answer,
            error=None,
        )