from __future__ import annotations

from app.agents.prediction_agent.prediction_agent import (
    PredictionAgent,
)
from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)


__all__ = (
    "get_prediction_agent",
)


def get_prediction_agent(
    *,
    sql_agent: SQLAgent,
) -> PredictionAgent:
    """
    Build and return the PredictionAgent.

    Args:
        sql_agent:
            SQL Agent used to retrieve historical data.

    Returns:
        Configured PredictionAgent instance.
    """

    return PredictionAgent(
        sql_agent=sql_agent,
    )