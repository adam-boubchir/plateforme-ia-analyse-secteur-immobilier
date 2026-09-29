from __future__ import annotations

from pydantic import BaseModel, Field


__all__ = (
    "PredictionRequest",
)


class PredictionRequest(BaseModel):
    """
    Request received by the Prediction Agent.

    This model describes the parameters required to
    perform a prediction from historical data.
    """

    # ==========================================================
    # TARGET
    # ==========================================================

    target_column: str = Field(
        min_length=1,
        description="Column containing the value to predict.",
    )

    # ==========================================================
    # TIME
    # ==========================================================

    time_column: str = Field(
        min_length=1,
        description="Column representing the time dimension.",
    )

    # ==========================================================
    # HORIZON
    # ==========================================================

    forecast_horizon: int = Field(
        default=3,
        ge=1,
        description="Number of future periods to predict.",
    )

    # ==========================================================
    # DATA
    # ==========================================================

    rows: list[dict[str, object]] = Field(
        default_factory=list,
        description="Historical data used for prediction.",
    )

    # ==========================================================
    # OPTIONAL CONTEXT
    # ==========================================================

    filters: dict[str, object] = Field(
        default_factory=dict,
        description="Optional filters applied to the historical data.",
    )