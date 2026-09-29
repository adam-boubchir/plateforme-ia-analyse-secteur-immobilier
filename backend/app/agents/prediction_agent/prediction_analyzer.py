from __future__ import annotations

from typing import Any

from app.agents.prediction_agent.prediction_models import (
    PredictionResult,
)


__all__ = (
    "PredictionAnalyzer",
)


class PredictionAnalyzer:
    """
    Analyze prediction results and extract useful insights.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def analyze(
        self,
        *,
        prediction_result: PredictionResult,
    ) -> dict[str, Any]:
        """
        Analyze a prediction result.

        Returns:
            Dictionary containing prediction insights.
        """

        if not prediction_result.success:
            return {
                "success": False,
                "trend": None,
                "message": prediction_result.error
                or "Prediction failed.",
            }

        predictions = prediction_result.predictions

        if not predictions:
            return {
                "success": False,
                "trend": None,
                "message": "No predictions available.",
            }

        values = [
            prediction.predicted_value
            for prediction in predictions
        ]

        trend = self._detect_trend(
            values=values,
        )

        evolution = self._calculate_evolution(
            values=values,
        )

        confidence = self._analyze_confidence(
            prediction_result=prediction_result,
        )

        return {
            "success": True,
            "trend": trend,
            "first_value": values[0],
            "last_value": values[-1],
            "absolute_change": evolution["absolute_change"],
            "percentage_change": evolution["percentage_change"],
            "confidence": confidence,
            "prediction_count": len(predictions),
        }

    # ==========================================================
    # TREND
    # ==========================================================

    @staticmethod
    def _detect_trend(
        *,
        values: list[float],
    ) -> str:
        """
        Detect the overall prediction trend.
        """

        if len(values) < 2:
            return "stable"

        first_value = values[0]
        last_value = values[-1]

        difference = last_value - first_value

        tolerance = abs(first_value) * 0.01

        if difference > tolerance:
            return "increasing"

        if difference < -tolerance:
            return "decreasing"

        return "stable"

    # ==========================================================
    # EVOLUTION
    # ==========================================================

    @staticmethod
    def _calculate_evolution(
        *,
        values: list[float],
    ) -> dict[str, float]:
        """
        Calculate absolute and percentage evolution.
        """

        first_value = values[0]
        last_value = values[-1]

        absolute_change = (
            last_value - first_value
        )

        if first_value == 0:
            percentage_change = 0.0
        else:
            percentage_change = (
                absolute_change / abs(first_value)
            ) * 100

        return {
            "absolute_change": absolute_change,
            "percentage_change": percentage_change,
        }

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    @staticmethod
    def _analyze_confidence(
        *,
        prediction_result: PredictionResult,
    ) -> dict[str, float | None]:
        """
        Analyze prediction confidence intervals.
        """

        predictions = prediction_result.predictions

        widths: list[float] = []

        for prediction in predictions:

            if (
                prediction.lower_bound is not None
                and prediction.upper_bound is not None
            ):

                width = (
                    prediction.upper_bound
                    - prediction.lower_bound
                )

                widths.append(
                    width,
                )

        if not widths:
            return {
                "average_interval_width": None,
                "min_interval_width": None,
                "max_interval_width": None,
            }

        return {
            "average_interval_width": (
                sum(widths) / len(widths)
            ),
            "min_interval_width": min(widths),
            "max_interval_width": max(widths),
        }