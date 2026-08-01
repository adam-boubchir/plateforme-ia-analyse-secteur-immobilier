from app.agents.chat_agent.chat_agent import (
    ChatAgent,
)
from app.agents.orchestrator.orchestrator_schema import (
    AgentType,
)
from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)


class AgentRegistry:
    """
    Registry responsible for providing the appropriate AI agent
    based on the orchestrator decision.
    """

    def __init__(
        self,
        sql_agent: SQLAgent,
        chat_agent: ChatAgent,
    ) -> None:

        self._agents: dict[AgentType, object] = {
            AgentType.SQL: sql_agent,
            AgentType.CHAT: chat_agent,
        }

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get(
        self,
        agent_type: AgentType,
    ) -> object:
        """
        Return the corresponding AI agent.
        """

        agent = self._agents.get(agent_type)

        if agent is None:
            raise ValueError(
                f"No agent registered for '{agent_type}'."
            )

        return agent

    def register(
        self,
        agent_type: AgentType,
        agent: object,
    ) -> None:
        """
        Register a new AI agent.
        """

        self._agents[agent_type] = agent