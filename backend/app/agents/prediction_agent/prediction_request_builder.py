from __future__ import annotations

import re
from typing import Any

from app.agents.prediction_agent.prediction_request import (
    PredictionRequest,
)


__all__ = (
    "PredictionRequestBuilder",
)


class PredictionRequestBuilder:
    """
    Build a PredictionRequest from a user question and
    historical SQL rows.

    Responsibilities:
        - Detect the time column.
        - Detect the numeric target column.
        - Detect the forecast horizon.
        - Build a validated PredictionRequest.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        question: str,
        rows: list[dict[str, Any]],
    ) -> PredictionRequest:
        """
        Build a PredictionRequest from SQL results.

        Args:
            question:
                Original user question.

            rows:
                Historical rows returned by SQL Agent.

        Returns:
            Structured PredictionRequest.
        """

        if not rows:
            raise ValueError(
                "Aucune donnée historique disponible "
                "pour effectuer une prédiction."
            )

        columns = self._get_columns(
            rows=rows,
        )

        time_column = self._detect_time_column(
            columns=columns,
        )

        target_column = self._detect_target_column(
            columns=columns,
            rows=rows,
            time_column=time_column,
        )

        forecast_horizon = self._detect_forecast_horizon(
            question=question,
        )

        return PredictionRequest(
            target_column=target_column,
            time_column=time_column,
            forecast_horizon=forecast_horizon,
            rows=rows,
        )

    # ==========================================================
    # COLUMNS
    # ==========================================================

    @staticmethod
    def _get_columns(
        *,
        rows: list[dict[str, Any]],
    ) -> list[str]:
        """
        Extract all available columns.
        """

        columns: list[str] = []

        for row in rows:

            for column in row.keys():

                if column not in columns:

                    columns.append(
                        column,
                    )

        return columns

    # ==========================================================
    # TIME COLUMN
    # ==========================================================

    @staticmethod
    def _detect_time_column(
        *,
        columns: list[str],
    ) -> str:
        """
        Detect the temporal column.
        """

        time_keywords = (
            "annee",
            "année",
            "year",
            "date",
            "mois",
            "month",
            "periode",
            "période",
            "trimestre",
            "quarter",
            "temps",
        )

        for column in columns:

            normalized_column = column.lower()

            if any(
                keyword in normalized_column
                for keyword in time_keywords
            ):
                return column

        raise ValueError(
            "Impossible d'identifier une colonne temporelle "
            "dans les données historiques."
        )

    # ==========================================================
    # TARGET COLUMN
    # ==========================================================

    def _detect_target_column(
        self,
        *,
        columns: list[str],
        rows: list[dict[str, Any]],
        time_column: str,
    ) -> str:
        """
        Detect the numeric column to predict.
        """

        preferred_keywords = (
            "prix",
            "price",
            "valeur",
            "value",
            "montant",
            "indice",
            "loyer",
            "cout",
            "coût",
            "consommation",
            "nombre",
            "total",
        )

        for column in columns:

            if column == time_column:
                continue

            normalized_column = column.lower()

            if any(
                keyword in normalized_column
                for keyword in preferred_keywords
            ):

                if self._is_numeric_column(
                    rows=rows,
                    column=column,
                ):
                    return column

        for column in columns:

            if column == time_column:
                continue

            if self._is_numeric_column(
                rows=rows,
                column=column,
            ):
                return column

        raise ValueError(
            "Impossible d'identifier une colonne numérique "
            "à prédire."
        )

    @staticmethod
    def _is_numeric_column(
        *,
        rows: list[dict[str, Any]],
        column: str,
    ) -> bool:
        """
        Determine whether a column contains numeric values.
        """

        values = [
            row.get(column)
            for row in rows
            if row.get(column) is not None
        ]

        if not values:
            return False

        numeric_count = 0

        for value in values:

            try:

                float(
                    str(value).replace(",", ".")
                )

                numeric_count += 1

            except (
                ValueError,
                TypeError,
            ):
                continue

        return (
            numeric_count / len(values)
        ) >= 0.7

    # ==========================================================
    # FORECAST HORIZON
    # ==========================================================

    @staticmethod
    def _detect_forecast_horizon(
        *,
        question: str,
    ) -> int:
        """
        Detect the number of future periods requested
        by the user.

        Default: 3.
        """

        match = re.search(
            r"\b(\d+)\s*(ans?|années?|years?|mois|months?|"
            r"trimestres?|quarters?)\b",
            question.lower(),
        )

        if match:

            return int(
                match.group(1)
            )

        return 3