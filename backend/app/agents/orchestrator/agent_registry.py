from __future__ import annotations

from collections.abc import Mapping

from app.agents.base.base_agent import BaseAgent
from app.agents.chat_agent.chat_agent import ChatAgent
from app.agents.orchestrator.orchestrator_schema import AgentType
from app.agents.report_agent.report_agent import ReportAgent
from app.agents.sql_agent.sql_agent import SQLAgent

__all__ = (
    "AgentRegistry",
)


class AgentRegistry:
    """
    Registry responsible for storing and resolving AI agents.

    This registry acts as the central lookup mechanism for the
    OrchestratorService. Each AgentType is associated with a single
    BaseAgent implementation.

    New agents can be registered dynamically without modifying the
    orchestrator.
    """

    def __init__(
        self,
        *,
        sql_agent: SQLAgent,
        chat_agent: ChatAgent,
        report_agent: ReportAgent,
    ) -> None:
        self._agents: dict[AgentType, BaseAgent] = {}

        self.register(
            agent_type=AgentType.SQL,
            agent=sql_agent,
        )

        self.register(
            agent_type=AgentType.CHAT,
            agent=chat_agent,
        )

        self.register(
            agent_type=AgentType.REPORT,
            agent=report_agent,
        )

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def get(
        self,
        *,
        agent_type: AgentType,
    ) -> BaseAgent:
        """
        Return the registered agent associated with the given type.

        Raises
        ------
        KeyError
            If no agent is registered for the requested type.
        """

        try:
            return self._agents[agent_type]

        except KeyError as ex:
            raise KeyError(
                f"No agent registered for '{agent_type.value}'.",
            ) from ex

    def register(
        self,
        *,
        agent_type: AgentType,
        agent: BaseAgent,
    ) -> None:
        """
        Register or replace an agent implementation.
        """

        self._agents[agent_type] = agent

    def unregister(
        self,
        *,
        agent_type: AgentType,
    ) -> None:
        """
        Remove a registered agent.

        Raises
        ------
        KeyError
            If the agent is not registered.
        """

        del self._agents[agent_type]

    def contains(
        self,
        *,
        agent_type: AgentType,
    ) -> bool:
        """
        Return whether an agent is registered.
        """

        return agent_type in self._agents

    @property
    def agents(
        self,
    ) -> Mapping[AgentType, BaseAgent]:
        """
        Return a read-only view of the registered agents.
        """

        return self._agents.copy()