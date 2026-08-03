from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

__all__ = (
    "AgentType",
    "OrchestratorDecision",
)


class AgentType(str, Enum):
    """
    Enumeration of all available AI agents.
    """

    SQL = "sql_agent"
    CHAT = "chat_agent"
    DASHBOARD = "dashboard_agent"
    PREDICTION = "prediction_agent"
    BENCHMARK = "benchmark_agent"
    REPORT = "report_agent"


class OrchestratorDecision(BaseModel):
    """
    Routing decision returned by the Orchestrator.
    """

    model_config = ConfigDict(
        frozen=True,
    )

    agent: AgentType = Field(
        ...,
        description="Selected AI agent.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0.",
    )

    reason: str = Field(
        ...,
        min_length=1,
        description="Reason explaining why the selected agent was selected.",
    )