from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


__all__ = (
    "PredictionPoint",
    "PredictionResult",
)


class PredictionPoint(BaseModel):
    """
    One predicted value for a future time period.
    """

    # ==========================================================
    # TIME
    # ==========================================================

    period: Any

    # ==========================================================
    # PREDICTION
    # ==========================================================

    predicted_value: float

    # ==========================================================
    # CONFIDENCE INTERVAL
    # ==========================================================

    lower_bound: float | None = None

    upper_bound: float | None = None


class PredictionResult(BaseModel):
    """
    Result produced by the Prediction Engine.
    """

    # ==========================================================
    # STATUS
    # ==========================================================

    success: bool = True

    error: str | None = None

    # ==========================================================
    # TARGET
    # ==========================================================

    target_column: str

    time_column: str

    # ==========================================================
    # MODEL
    # ==========================================================

    model_name: str

    # ==========================================================
    # FORECAST
    # ==========================================================

    forecast_horizon: int

    predictions: list[PredictionPoint] = Field(
        default_factory=list,
    )

    # ==========================================================
    # PERFORMANCE
    # ==========================================================

    metrics: dict[str, float] = Field(
        default_factory=dict,
    )

    # ==========================================================
    # ADDITIONAL INFORMATION
    # ==========================================================

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )