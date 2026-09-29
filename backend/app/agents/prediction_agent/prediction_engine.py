from __future__ import annotations

from typing import Any

import pandas as pd
from prophet import Prophet

from app.agents.prediction_agent.prediction_models import (
    PredictionPoint,
    PredictionResult,
)


__all__ = (
    "PredictionEngine",
)


class PredictionEngine:
    """
    Prediction engine responsible for generating forecasts
    from historical time-series data.

    Current implementation:
        - Uses Prophet.
        - Converts historical rows to a Prophet DataFrame.
        - Trains the model.
        - Generates future predictions.
        - Returns PredictionResult.

    Expected Prophet format:
        ds -> datetime column
        y  -> numeric target column
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def predict(
        self,
        *,
        target_column: str,
        time_column: str,
        forecast_horizon: int,
        rows: list[dict[str, object]],
    ) -> PredictionResult:
        """
        Generate predictions from historical data.

        Args:
            target_column:
                Column containing the values to predict.

            time_column:
                Column representing time.

            forecast_horizon:
                Number of future periods to predict.

            rows:
                Historical data.

        Returns:
            PredictionResult containing future predictions.
        """

        try:

            # ==================================================
            # VALIDATION
            # ==================================================

            self._validate_input(
                target_column=target_column,
                time_column=time_column,
                forecast_horizon=forecast_horizon,
                rows=rows,
            )

            # ==================================================
            # PREPARE DATA
            # ==================================================

            dataframe = self._build_dataframe(
                rows=rows,
                time_column=time_column,
                target_column=target_column,
            )

            # ==================================================
            # VALIDATE DATA
            # ==================================================

            if len(dataframe) < 2:

                raise ValueError(
                    "Au moins 2 données historiques sont "
                    "nécessaires pour effectuer une prédiction."
                )

            # ==================================================
            # DETECT FREQUENCY
            # ==================================================

            frequency = self._detect_frequency(
                dataframe=dataframe,
            )

            # ==================================================
            # TRAIN MODEL
            # ==================================================

            model = Prophet(
                interval_width=0.95,
            )

            model.fit(
                dataframe,
            )

            # ==================================================
            # CREATE FUTURE DATAFRAME
            # ==================================================

            future = model.make_future_dataframe(
                periods=forecast_horizon,
                freq=frequency,
            )

            # ==================================================
            # GENERATE FORECAST
            # ==================================================

            forecast = model.predict(
                future,
            )

            # ==================================================
            # EXTRACT FUTURE PREDICTIONS
            # ==================================================

            future_forecast = forecast.tail(
                forecast_horizon,
            )

            predictions = self._build_predictions(
                forecast=future_forecast,
                frequency=frequency,
            )

            # ==================================================
            # METRICS
            # ==================================================

            metrics = self._calculate_metrics(
                model=model,
                dataframe=dataframe,
            )

            # ==================================================
            # METADATA
            # ==================================================

            metadata = {
                "historical_rows": len(dataframe),
                "frequency": frequency,
                "last_historical_period": (
                    self._format_period(
                        dataframe["ds"].max(),
                        frequency=frequency,
                    )
                ),
                "forecast_horizon": forecast_horizon,
            }

            # ==================================================
            # SUCCESS RESULT
            # ==================================================

            return PredictionResult(
                success=True,
                error=None,
                target_column=target_column,
                time_column=time_column,
                model_name="Prophet",
                forecast_horizon=forecast_horizon,
                predictions=predictions,
                metrics=metrics,
                metadata=metadata,
            )

        except Exception as ex:

            return PredictionResult(
                success=False,
                error=str(ex),
                target_column=target_column,
                time_column=time_column,
                model_name="Prophet",
                forecast_horizon=forecast_horizon,
                predictions=[],
                metrics={},
                metadata={},
            )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @staticmethod
    def _validate_input(
        *,
        target_column: str,
        time_column: str,
        forecast_horizon: int,
        rows: list[dict[str, object]],
    ) -> None:
        """
        Validate prediction input.
        """

        if not rows:

            raise ValueError(
                "Aucune donnée historique disponible "
                "pour effectuer une prédiction."
            )

        if not target_column.strip():

            raise ValueError(
                "La colonne cible est obligatoire."
            )

        if not time_column.strip():

            raise ValueError(
                "La colonne temporelle est obligatoire."
            )

        if forecast_horizon < 1:

            raise ValueError(
                "L'horizon de prédiction doit être supérieur "
                "à zéro."
            )

    # ==========================================================
    # DATAFRAME
    # ==========================================================

    def _build_dataframe(
        self,
        *,
        rows: list[dict[str, object]],
        time_column: str,
        target_column: str,
    ) -> pd.DataFrame:
        """
        Convert historical rows to Prophet format.

        Prophet requires:

            ds -> datetime
            y  -> numeric value
        """

        data: list[dict[str, Any]] = []

        for row in rows:

            time_value = row.get(
                time_column,
            )

            target_value = row.get(
                target_column,
            )

            if (
                time_value is None
                or target_value is None
            ):
                continue

            parsed_time = self._parse_time(
                value=time_value,
            )

            parsed_target = self._parse_numeric(
                value=target_value,
            )

            if (
                parsed_time is None
                or parsed_target is None
            ):
                continue

            data.append(
                {
                    "ds": parsed_time,
                    "y": parsed_target,
                }
            )

        if not data:

            raise ValueError(
                "Impossible de préparer les données "
                "pour Prophet."
            )

        dataframe = pd.DataFrame(
            data,
        )

        # ======================================================
        # REMOVE INVALID VALUES
        # ======================================================

        dataframe = dataframe.dropna(
            subset=[
                "ds",
                "y",
            ],
        )

        # ======================================================
        # SORT BY TIME
        # ======================================================

        dataframe = dataframe.sort_values(
            by="ds",
        )

        # ======================================================
        # REMOVE DUPLICATES
        # ======================================================

        dataframe = (
            dataframe
            .groupby(
                "ds",
                as_index=False,
            )
            ["y"]
            .mean()
        )

        dataframe = dataframe.sort_values(
            by="ds",
        )

        dataframe = dataframe.reset_index(
            drop=True,
        )

        return dataframe

    # ==========================================================
    # TIME PARSING
    # ==========================================================

    @staticmethod
    def _parse_time(
        *,
        value: object,
    ) -> pd.Timestamp | None:
        """
        Convert a time value to pandas Timestamp.

        Supports:
            - 2020
            - "2020"
            - "2020-01-01"
            - normal date values
        """

        try:

            # ==================================================
            # INTEGER YEAR
            # ==================================================

            if isinstance(
                value,
                int,
            ):

                if 1000 <= value <= 3000:

                    return pd.Timestamp(
                        year=value,
                        month=1,
                        day=1,
                    )

            # ==================================================
            # FLOAT YEAR
            # ==================================================

            if isinstance(
                value,
                float,
            ):

                integer_value = int(
                    value,
                )

                if (
                    value == integer_value
                    and 1000 <= integer_value <= 3000
                ):

                    return pd.Timestamp(
                        year=integer_value,
                        month=1,
                        day=1,
                    )

            # ==================================================
            # STRING YEAR
            # ==================================================

            text_value = str(
                value,
            ).strip()

            if (
                text_value.isdigit()
                and len(text_value) == 4
            ):

                year = int(
                    text_value,
                )

                return pd.Timestamp(
                    year=year,
                    month=1,
                    day=1,
                )

            # ==================================================
            # NORMAL DATE
            # ==================================================

            parsed = pd.to_datetime(
                value,
                errors="coerce",
            )

            if pd.isna(
                parsed,
            ):

                return None

            return parsed

        except Exception:

            return None

    # ==========================================================
    # NUMERIC PARSING
    # ==========================================================

    @staticmethod
    def _parse_numeric(
        *,
        value: object,
    ) -> float | None:
        """
        Convert a value to float.
        """

        try:

            if isinstance(
                value,
                str,
            ):

                value = (
                    value
                    .strip()
                    .replace(" ", "")
                    .replace(",", ".")
                )

            numeric_value = float(
                value,
            )

            return numeric_value

        except (
            ValueError,
            TypeError,
        ):

            return None

    # ==========================================================
    # FREQUENCY DETECTION
    # ==========================================================

    @staticmethod
    def _detect_frequency(
        *,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Detect the time frequency.

        Possible values:
            YS -> yearly
            MS -> monthly
            D  -> daily

        Default:
            YS
        """

        if len(dataframe) < 2:

            return "YS"

        dates = (
            dataframe["ds"]
            .sort_values()
            .tolist()
        )

        differences: list[float] = []

        for index in range(
            1,
            len(dates),
        ):

            difference = (
                dates[index]
                - dates[index - 1]
            ).days

            if difference > 0:

                differences.append(
                    difference,
                )

        if not differences:

            return "YS"

        average_difference = (
            sum(differences)
            / len(differences)
        )

        # ======================================================
        # YEARLY
        # ======================================================

        if average_difference >= 300:

            return "YS"

        # ======================================================
        # MONTHLY
        # ======================================================

        if average_difference >= 25:

            return "MS"

        # ======================================================
        # DAILY
        # ======================================================

        return "D"

    # ==========================================================
    # BUILD PREDICTIONS
    # ==========================================================

    def _build_predictions(
        self,
        *,
        forecast: pd.DataFrame,
        frequency: str,
    ) -> list[PredictionPoint]:
        """
        Convert Prophet forecast to PredictionPoint objects.
        """

        predictions: list[PredictionPoint] = []

        for _, row in forecast.iterrows():

            period = self._format_period(
                row["ds"],
                frequency=frequency,
            )

            prediction = PredictionPoint(
                period=period,
                predicted_value=float(
                    row["yhat"],
                ),
                lower_bound=float(
                    row["yhat_lower"],
                ),
                upper_bound=float(
                    row["yhat_upper"],
                ),
            )

            predictions.append(
                prediction,
            )

        return predictions

    # ==========================================================
    # FORMAT PERIOD
    # ==========================================================

    @staticmethod
    def _format_period(
        value: pd.Timestamp,
        *,
        frequency: str,
    ) -> str:
        """
        Format a prediction period according
        to the detected frequency.
        """

        if frequency == "YS":

            return str(
                value.year,
            )

        if frequency == "MS":

            return (
                f"{value.year}-"
                f"{value.month:02d}"
            )

        return value.strftime(
            "%Y-%m-%d",
        )

    # ==========================================================
    # METRICS
    # ==========================================================

    @staticmethod
    def _calculate_metrics(
        *,
        model: Prophet,
        dataframe: pd.DataFrame,
    ) -> dict[str, float]:
        """
        Calculate simple training metrics.

        These metrics evaluate the model against
        the historical training data.

        Returns:
            MAE
            RMSE
            MAPE
        """

        try:

            forecast = model.predict(
                dataframe[["ds"]],
            )

            actual_values = (
                dataframe["y"]
                .astype(float)
                .tolist()
            )

            predicted_values = (
                forecast["yhat"]
                .astype(float)
                .tolist()
            )

            errors = [
                actual - predicted
                for actual, predicted
                in zip(
                    actual_values,
                    predicted_values,
                )
            ]

            # ==================================================
            # MAE
            # ==================================================

            mae = (
                sum(
                    abs(error)
                    for error in errors
                )
                / len(errors)
            )

            # ==================================================
            # RMSE
            # ==================================================

            mse = (
                sum(
                    error ** 2
                    for error in errors
                )
                / len(errors)
            )

            rmse = mse ** 0.5

            # ==================================================
            # MAPE
            # ==================================================

            percentage_errors: list[float] = []

            for actual, predicted in zip(
                actual_values,
                predicted_values,
            ):

                if actual != 0:

                    error = (
                        abs(
                            (
                                actual
                                - predicted
                            )
                            / actual
                        )
                        * 100
                    )

                    percentage_errors.append(
                        error,
                    )

            if percentage_errors:

                mape = (
                    sum(
                        percentage_errors,
                    )
                    / len(
                        percentage_errors,
                    )
                )

            else:

                mape = 0.0

            return {
                "mae": round(
                    float(mae),
                    4,
                ),
                "rmse": round(
                    float(rmse),
                    4,
                ),
                "mape": round(
                    float(mape),
                    4,
                ),
            }

        except Exception:

            # Metrics should never block prediction.

            return {}