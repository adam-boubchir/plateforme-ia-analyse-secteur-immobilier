from __future__ import annotations

from datetime import datetime
from typing import Any

from app.agents.prediction_agent.prediction_models import (
    PredictionResult,
)


__all__ = (
    "PredictionFormatter",
)


class PredictionFormatter:
    """
    Format prediction results into a human-readable response.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def format(
        self,
        *,
        prediction_result: PredictionResult,
        analysis: dict[str, Any],
    ) -> str:
        """
        Format prediction results into a natural language response.
        """

        # ======================================================
        # ERROR
        # ======================================================

        if not prediction_result.success:
            return self._format_error(
                prediction_result=prediction_result,
            )

        # ======================================================
        # ANALYSIS VALIDATION
        # ======================================================

        if not analysis.get("success"):
            return (
                "La prédiction a été générée, "
                "mais son analyse n'a pas pu être effectuée."
            )

        lines: list[str] = []

        # ======================================================
        # TITLE
        # ======================================================

        lines.append(
            "## 📈 Résultat de la prédiction"
        )

        lines.append("")

        # ======================================================
        # SUMMARY
        # ======================================================

        lines.append(
            self._format_summary(
                prediction_result=prediction_result,
                analysis=analysis,
            )
        )

        lines.append("")

        # ======================================================
        # PREDICTIONS
        # ======================================================

        lines.append(
            "### 📅 Prévisions"
        )

        lines.append("")

        lines.extend(
            self._format_predictions_table(
                prediction_result=prediction_result,
            )
        )

        lines.append("")

        # ======================================================
        # TREND
        # ======================================================

        lines.append(
            "### 📊 Analyse de la tendance"
        )

        lines.append("")

        lines.append(
            self._format_trend(
                analysis=analysis,
            )
        )

        lines.append("")

        # ======================================================
        # INFORMATION
        # ======================================================

        lines.append(
            "### ℹ️ Informations"
        )

        lines.append("")

        lines.extend(
            self._format_metadata(
                prediction_result=prediction_result,
            )
        )

        return "\n".join(
            lines,
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    @staticmethod
    def _format_error(
        *,
        prediction_result: PredictionResult,
    ) -> str:
        """
        Format a prediction error.
        """

        error = (
            prediction_result.error
            or "Erreur inconnue."
        )

        return (
            "## ❌ Erreur de prédiction\n\n"
            "Impossible de générer la prédiction.\n\n"
            f"**Détail :** {error}"
        )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def _format_summary(
        self,
        *,
        prediction_result: PredictionResult,
        analysis: dict[str, Any],
    ) -> str:
        """
        Build a natural prediction summary.
        """

        trend = self._translate_trend(
            trend=analysis.get("trend"),
        )

        percentage_change = float(
            analysis.get(
                "percentage_change",
                0.0,
            )
        )

        evolution = self._format_signed_value(
            value=percentage_change,
            suffix="%",
        )

        return (
            f"Les prévisions indiquent une tendance "
            f"**{trend}** sur les "
            f"**{prediction_result.forecast_horizon} "
            f"prochaines périodes**. "
            f"L'évolution estimée est de "
            f"**{evolution}**."
        )

    # ==========================================================
    # PREDICTIONS TABLE
    # ==========================================================

    def _format_predictions_table(
        self,
        *,
        prediction_result: PredictionResult,
    ) -> list[str]:
        """
        Format predictions as a Markdown table.
        """

        lines = [
            "| Période | Valeur prédite | Intervalle estimé |",
            "|---|---:|---|",
        ]

        for prediction in prediction_result.predictions:

            period = self._format_period(
                period=prediction.period,
            )

            predicted_value = (
                prediction.predicted_value
            )

            interval = self._format_interval(
                lower_bound=prediction.lower_bound,
                upper_bound=prediction.upper_bound,
            )

            lines.append(
                f"| {period} | "
                f"{predicted_value:.2f} | "
                f"{interval} |"
            )

        return lines

    # ==========================================================
    # PERIOD
    # ==========================================================

    @staticmethod
    def _format_period(
        *,
        period: Any,
    ) -> str:
        """
        Format a prediction period for display.
        """

        if isinstance(
            period,
            datetime,
        ):
            return str(period.year)

        if hasattr(
            period,
            "year",
        ):
            return str(period.year)

        period_text = str(period)

        if len(period_text) >= 4:
            return period_text[:4]

        return period_text

    # ==========================================================
    # INTERVAL
    # ==========================================================

    @staticmethod
    def _format_interval(
        *,
        lower_bound: float | None,
        upper_bound: float | None,
    ) -> str:
        """
        Format confidence interval.
        """

        if (
            lower_bound is None
            or upper_bound is None
        ):
            return "Non disponible"

        return (
            f"{lower_bound:.2f} → "
            f"{upper_bound:.2f}"
        )

    # ==========================================================
    # TREND
    # ==========================================================

    def _format_trend(
        self,
        *,
        analysis: dict[str, Any],
    ) -> str:
        """
        Format trend analysis.
        """

        trend = analysis.get(
            "trend",
        )

        trend_text = self._translate_trend(
            trend=trend,
        )

        first_value = float(
            analysis.get(
                "first_value",
                0.0,
            )
        )

        last_value = float(
            analysis.get(
                "last_value",
                0.0,
            )
        )

        absolute_change = float(
            analysis.get(
                "absolute_change",
                0.0,
            )
        )

        percentage_change = float(
            analysis.get(
                "percentage_change",
                0.0,
            )
        )

        absolute_change_text = (
            self._format_signed_value(
                value=absolute_change,
            )
        )

        percentage_change_text = (
            self._format_signed_value(
                value=percentage_change,
                suffix="%",
            )
        )

        return (
            f"La tendance globale est **{trend_text}**. "
            f"La valeur prédite devrait passer de "
            f"**{first_value:.2f}** à "
            f"**{last_value:.2f}**, "
            f"soit une variation de "
            f"**{absolute_change_text}** "
            f"(**{percentage_change_text}**)."
        )

    # ==========================================================
    # METADATA
    # ==========================================================

    @staticmethod
    def _format_metadata(
        *,
        prediction_result: PredictionResult,
    ) -> list[str]:
        """
        Format technical prediction information.
        """

        metadata = prediction_result.metadata

        historical_rows = metadata.get(
            "historical_rows",
        )

        selected_model = metadata.get(
            "selected_model",
        )

        lines = [
            (
                f"- **Modèle utilisé :** "
                f"{prediction_result.model_name}"
            ),
            (
                f"- **Périodes prédites :** "
                f"{prediction_result.forecast_horizon}"
            ),
        ]

        if selected_model is not None:

            lines.append(
                (
                    f"- **Modèle sélectionné :** "
                    f"{selected_model}"
                )
            )

        if historical_rows is not None:

            lines.append(
                (
                    f"- **Observations historiques "
                    f"utilisées :** {historical_rows}"
                )
            )

        return lines

    # ==========================================================
    # UTILITIES
    # ==========================================================

    @staticmethod
    def _format_signed_value(
        *,
        value: float,
        suffix: str = "",
    ) -> str:
        """
        Format a value with an explicit sign.
        """

        if value > 0:
            return f"+{value:.2f}{suffix}"

        return f"{value:.2f}{suffix}"

    @staticmethod
    def _translate_trend(
        *,
        trend: str | None,
    ) -> str:
        """
        Translate internal trend value into French.
        """

        translations = {
            "increasing": "à la hausse",
            "decreasing": "à la baisse",
            "stable": "stable",
        }

        return translations.get(
            trend,
            "non déterminée",
        )