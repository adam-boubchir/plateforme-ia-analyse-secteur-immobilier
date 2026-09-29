from __future__ import annotations


__all__ = (
    "ModelSelector",
)


class ModelSelector:
    """
    Select the most appropriate prediction model.

    The current version focuses on time-series prediction
    and selects Prophet.

    This component is designed to be extended later with
    additional models such as XGBoost or other forecasting
    algorithms.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        *,
        rows: list[dict[str, object]],
        time_column: str,
        target_column: str,
    ) -> str:
        """
        Select a prediction model according to the
        available historical data.

        Args:
            rows:
                Historical data.

            time_column:
                Column representing the time dimension.

            target_column:
                Column containing the value to predict.

        Returns:
            Name of the selected model.
        """

        self._validate_input(
            rows=rows,
            time_column=time_column,
            target_column=target_column,
        )

        return "Prophet"

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @staticmethod
    def _validate_input(
        *,
        rows: list[dict[str, object]],
        time_column: str,
        target_column: str,
    ) -> None:
        """
        Validate the data before model selection.
        """

        if not rows:
            raise ValueError(
                "Aucune donnée historique disponible "
                "pour sélectionner un modèle."
            )

        if not time_column.strip():
            raise ValueError(
                "La colonne temporelle est obligatoire."
            )

        if not target_column.strip():
            raise ValueError(
                "La colonne cible est obligatoire."
            )