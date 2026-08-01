from __future__ import annotations

import json

from app.agents.orchestrator.orchestrator_schema import (
    AgentType,
    OrchestratorDecision,
)
from app.services.llm_service import LLMService

__all__ = ["OrchestratorGenerator"]


class OrchestratorGenerator:
    """
    Generate routing decisions using the configured LLM.

    Responsibilities:
        - Send the routing prompt to the LLM.
        - Parse the JSON response.
        - Return a validated OrchestratorDecision.
    """

    AGENT_NAME = "orchestrator"

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self.llm_service = llm_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        prompt: str,
    ) -> OrchestratorDecision:
        """
        Generate the routing decision.

        Args:
            prompt: Prompt sent to the language model.

        Returns:
            Parsed OrchestratorDecision.
        """

        response = self.llm_service.generate(
            agent_name=self.AGENT_NAME,
            prompt=prompt,
        )

        return self._parse_response(response)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _parse_response(
        self,
        response: str,
    ) -> OrchestratorDecision:
        """
        Parse the JSON response returned by the language model.

        Args:
            response: Raw JSON string returned by the LLM.

        Returns:
            Parsed OrchestratorDecision. Falls back to the Chat Agent
            if parsing fails.
        """

        try:
            data = json.loads(response)

            return OrchestratorDecision(
                agent=AgentType(data["agent"]),
                confidence=float(data.get("confidence", 0.0)),
                reason=data.get("reason", ""),
            )

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ):
            return self._fallback_decision()

    def _fallback_decision(self) -> OrchestratorDecision:
        """
        Return the default routing decision when the LLM response
        cannot be parsed.
        """

        return OrchestratorDecision(
            agent=AgentType.CHAT,
            confidence=0.0,
            reason="Unable to parse LLM response.",
        )