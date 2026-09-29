from __future__ import annotations

import re


__all__ = (
    "PredictionQueryBuilder",
)


class PredictionQueryBuilder:
    """
    Build a historical-data retrieval question for the SQL Agent.

    The Prediction Agent receives a question about the future,
    but the SQL Agent must retrieve existing historical data.

    Example:

        User question:
        "Predict cement prices for the next 3 years."

        SQL question:
        "Retrieve the complete historical evolution of
        cement prices over time."
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
        Transform a prediction question into a historical
        data retrieval question.

        Args:
            question:
                Original prediction request.

        Returns:
            Question optimized for the SQL Agent.
        """

        subject = self._extract_subject(
            question=question,
        )

        return (
            "Retrieve all available historical data over time "
            f"related to: {subject}. "
            "The result must include the temporal column and "
            "the numeric value to be predicted. "
            "Return sufficient historical observations for "
            "time-series forecasting."
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _extract_subject(
        *,
        question: str,
    ) -> str:
        """
        Extract the subject of the prediction request.

        The current implementation removes common forecasting
        expressions while preserving the main business subject.
        """

        subject = question.strip()

        patterns = (
            r"\bpr[ée]di[rs]?\b",
            r"\bpr[ée]vision\b",
            r"\bforecast\b",
            r"\bestim[ée]r?\b",
            r"\bprojection\b",
            r"\bpour les?\s+\d+\s+prochain(?:e)?s?\s+"
            r"(ans?|ann[ée]es?|mois|trimestres?)\b",
            r"\bdans les?\s+\d+\s+"
            r"(ans?|ann[ée]es?|mois|trimestres?)\b",
            r"\bnext\s+\d+\s+"
            r"(years?|months?|quarters?)\b",
        )

        for pattern in patterns:

            subject = re.sub(
                pattern,
                "",
                subject,
                flags=re.IGNORECASE,
            )

        subject = re.sub(
            r"\s+",
            " ",
            subject,
        ).strip()

        if not subject:

            return question

        return subject