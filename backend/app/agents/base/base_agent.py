from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.agent_response import AgentResponse

__all__ = ["BaseAgent"]


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.

    Every agent in the platform must implement the `ask` method
    and return a standardized AgentResponse.
    """

    @abstractmethod
    def ask(
        self,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:
        """
        Process a user request and return a standardized response.

        Args:
            question: User natural language question.
            conversation_id: Conversation identifier.

        Returns:
            AgentResponse produced by the agent.
        """
        raise NotImplementedError