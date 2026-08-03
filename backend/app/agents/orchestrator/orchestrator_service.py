from __future__ import annotations

from app.agents.base.base_agent import BaseAgent
from app.agents.orchestrator.agent_registry import AgentRegistry
from app.agents.orchestrator.orchestrator_agent import OrchestratorAgent
from app.agents.orchestrator.orchestrator_schema import (
    OrchestratorDecision,
)
from app.models.agent_response import AgentResponse

__all__ = (
    "OrchestratorService",
)


class OrchestratorService:
    """
    Coordinate the routing workflow of the AI platform.

    Responsibilities
    ----------------
    - Ask the OrchestratorAgent which AI agent should handle the request.
    - Resolve the selected agent from the registry.
    - Execute the selected agent.
    - Return the unified AgentResponse.
    """

    def __init__(
        self,
        *,
        orchestrator_agent: OrchestratorAgent,
        agent_registry: AgentRegistry,
    ) -> None:
        self._orchestrator_agent = orchestrator_agent
        self._agent_registry = agent_registry

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def route(
        self,
        *,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:
        """
        Route a user request to the appropriate AI agent.
        """

        decision = self._orchestrator_agent.route(
            question=question,
        )

        self._log_decision(
            question=question,
            decision=decision,
        )

        agent = self._resolve_agent(
            decision=decision,
        )

        return agent.ask(
            question=question,
            conversation_id=conversation_id,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _resolve_agent(
        self,
        *,
        decision: OrchestratorDecision,
    ) -> BaseAgent:
        """
        Resolve the selected AI agent.
        """

        return self._agent_registry.get(
            agent_type=decision.agent,
        )

    @staticmethod
    def _log_decision(
        *,
        question: str,
        decision: OrchestratorDecision,
    ) -> None:
        """
        Log the routing decision.

        TODO:
            Replace print() with the application logger.
        """

        print("\n" + "=" * 80)
        print("ORCHESTRATOR")
        print(f"Question       : {question}")
        print(f"Selected Agent : {decision.agent.value}")
        print("=" * 80 + "\n")