from app.agents.orchestrator.agent_registry import (
    AgentRegistry,
)

from app.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
)

from app.models.agent_response import (
    AgentResponse,
)


class OrchestratorService:
    """
    Service responsible for routing user requests
    to the appropriate AI agent.

    Workflow
    --------
    User Question
          ↓
    OrchestratorAgent
          ↓
    OrchestratorDecision
          ↓
    AgentRegistry
          ↓
    Selected Agent
          ↓
    AgentResponse
    """

    def __init__(
        self,
        orchestrator_agent: OrchestratorAgent,
        agent_registry: AgentRegistry,
    ) -> None:

        self.orchestrator_agent: OrchestratorAgent = orchestrator_agent
        self.agent_registry: AgentRegistry = agent_registry

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def route(
        self,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:
        """
        Route the request to the appropriate AI agent.
        """

        decision = self.orchestrator_agent.route(
            question=question,
        )

        agent = self.agent_registry.get(
            decision.agent,
        )

        return agent.ask(
            question=question,
            conversation_id=conversation_id,
        )