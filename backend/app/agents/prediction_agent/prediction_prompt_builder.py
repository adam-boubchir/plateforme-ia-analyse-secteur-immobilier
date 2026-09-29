from __future__ import annotations

from typing import Any

from app.agents.prediction_agent.prediction_request import (
    PredictionRequest,
)


__all__ = (
    "PredictionPromptBuilder",
)


class PredictionPromptBuilder:
    """
    Build structured prompts for the Prediction Agent.

    This class is responsible only for constructing the
    textual context sent to the AI model.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build a prediction prompt from a prediction request.

        Args:
            request:
                Structured prediction request.

        Returns:
            Prompt ready to be sent to an AI model.
        """

        sections = [
            self._build_role_section(),
            self._build_target_section(
                request=request,
            ),
            self._build_time_section(
                request=request,
            ),
            self._build_horizon_section(
                request=request,
            ),
            self._build_filters_section(
                request=request,
            ),
            self._build_data_section(
                request=request,
            ),
            self._build_instructions_section(),
        ]

        prompt = "\n\n".join(
            section
            for section in sections
            if section
        )

        return prompt

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_role_section() -> str:
        """
        Build the role definition for the AI model.
        """

        return """
You are a forecasting assistant specialized in
real-estate and construction-sector data analysis.

Your task is to analyze historical time-series data
and provide a reliable basis for future-value prediction.
""".strip()

    @staticmethod
    def _build_target_section(
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build the target-variable section.
        """

        return f"""
TARGET VARIABLE
---------------
Column to predict: {request.target_column}
""".strip()

    @staticmethod
    def _build_time_section(
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build the time-variable section.
        """

        return f"""
TIME VARIABLE
-------------
Time column: {request.time_column}
""".strip()

    @staticmethod
    def _build_horizon_section(
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build the forecast-horizon section.
        """

        return f"""
FORECAST HORIZON
----------------
Number of future periods: {request.forecast_horizon}
""".strip()

    @staticmethod
    def _build_filters_section(
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build the optional filters section.
        """

        if not request.filters:
            return """
FILTERS
-------
No additional filters were specified.
""".strip()

        filters_text = "\n".join(
            f"- {key}: {value}"
            for key, value in request.filters.items()
        )

        return f"""
FILTERS
-------
{filters_text}
""".strip()

    @staticmethod
    def _build_data_section(
        *,
        request: PredictionRequest,
    ) -> str:
        """
        Build the historical-data section.
        """

        if not request.rows:
            return """
HISTORICAL DATA
---------------
No historical rows were provided.
""".strip()

        data_text = "\n".join(
            str(row)
            for row in request.rows
        )

        return f"""
HISTORICAL DATA
---------------
{data_text}
""".strip()

    @staticmethod
    def _build_instructions_section() -> str:
        """
        Build the final instructions for the AI model.
        """

        return """
INSTRUCTIONS
------------
1. Analyze the historical data according to the specified
   time column and target column.

2. Identify the temporal evolution of the target variable.

3. Consider the available historical observations before
   producing a forecast.

4. Do not invent historical observations.

5. Do not modify the provided historical data.

6. The final prediction will be produced by the dedicated
   prediction engine.

7. Provide structured reasoning that can be used by the
   Prediction Agent to select and configure an appropriate
   forecasting approach.
""".strip()