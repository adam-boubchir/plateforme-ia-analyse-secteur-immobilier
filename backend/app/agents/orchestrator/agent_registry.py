from __future__ import annotations

from collections.abc import Mapping

from app.agents.base.base_agent import BaseAgent

from app.agents.chat_agent.chat_agent import ChatAgent

from app.agents.orchestrator.orchestrator_schema import (
    AgentType,
)

from app.agents.prediction_agent.prediction_agent import (
    PredictionAgent,
)

from app.agents.report_agent.report_agent import ReportAgent

from app.agents.sql_agent.sql_agent import SQLAgent


__all__ = (
    "AgentRegistry",
)


class AgentRegistry:
    """
    Registry responsible for storing and resolving AI agents.

    Each AgentType is associated with a single
    BaseAgent implementation.
    """

    def __init__(
        self,
        *,
        sql_agent: SQLAgent,
        chat_agent: ChatAgent,
        report_agent: ReportAgent,
        prediction_agent: PredictionAgent,
    ) -> None:

        self._agents: dict[AgentType, BaseAgent] = {}

        # ======================================================
        # SQL AGENT
        # ======================================================

        self.register(
            agent_type=AgentType.SQL,
            agent=sql_agent,
        )

        # ======================================================
        # CHAT AGENT
        # ======================================================

        self.register(
            agent_type=AgentType.CHAT,
            agent=chat_agent,
        )

        # ======================================================
        # REPORT AGENT
        # ======================================================

        self.register(
            agent_type=AgentType.REPORT,
            agent=report_agent,
        )

        # ======================================================
        # PREDICTION AGENT
        # ======================================================

        self.register(
            agent_type=AgentType.PREDICTION,
            agent=prediction_agent,
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
        """

        try:

            return self._agents[
                agent_type
            ]

        except KeyError as ex:

            raise KeyError(
                f"No agent registered for "
                f"'{agent_type.value}'."
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

        self._agents[
            agent_type
        ] = agent

    def unregister(
        self,
        *,
        agent_type: AgentType,
    ) -> None:
        """
        Remove a registered agent.
        """

        del self._agents[
            agent_type
        ]

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
        Return a read-only view of registered agents.
        """

        return self._agents.copy()