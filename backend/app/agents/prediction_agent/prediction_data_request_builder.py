from __future__ import annotations


__all__ = (
    "PredictionDataRequestBuilder",
)


class PredictionDataRequestBuilder:
    """
    Build a historical data request for the SQL Agent.

    The Prediction Agent does not ask the SQL Agent to
    generate a prediction.

    Instead, it transforms the user's prediction request
    into a request for historical data.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        question: str,
    ) -> str:
        """
        Build a SQL-oriented request for retrieving
        historical data required for prediction.

        Args:
            question:
                Original user prediction request.

        Returns:
            Historical data request for SQL Agent.
        """

        return self._build_historical_request(
            question=question,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _build_historical_request(
        *,
        question: str,
    ) -> str:
        """
        Build the historical data retrieval request.
        """

        return f"""
The user wants to generate a future prediction.

Original user request:
{question}

Your task is NOT to generate a prediction.

Retrieve the historical time-series data required
to perform the prediction.

Requirements:

1. Return all available historical observations.

2. Include a temporal column such as:
   - year
   - date
   - month
   - quarter

3. Include the numeric variable that must be predicted.

4. Preserve the chronological evolution of the data.

5. Do not aggregate the data unless aggregation is
   required to build a valid time series.

6. Return enough historical observations to allow
   a forecasting model to analyze the trend.

The result must contain historical data only.
""".strip()