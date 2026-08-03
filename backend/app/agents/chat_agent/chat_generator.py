from __future__ import annotations

from app.services.llm_service import LLMService

__all__ = ("ChatGenerator",)


class ChatGenerator:
    """
    Generate responses for the Chat Agent using the configured LLM.
    """

    _AGENT_NAME = "chat_agent"

    def __init__(
        self,
        *,
        llm_service: LLMService,
    ) -> None:
        self._llm_service = llm_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        prompt: str,
    ) -> str:
        """
        Generate a response from the configured language model.

        Args:
            prompt: Prompt sent to the language model.

        Returns:
            Generated response with surrounding whitespace removed.
        """

        response = self._llm_service.generate(
            agent_name=self._AGENT_NAME,
            prompt=prompt,
        )

        return response.strip()