from __future__ import annotations


__all__ = (
    "FeatureBuilder",
)


class FeatureBuilder:
    """
    Prepare historical data before prediction.

    Responsibilities:
        - Validate rows.
        - Validate required columns.
        - Remove invalid rows.
        - Prepare data for the Prediction Engine.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(
        self,
        *,
        rows: list[dict[str, object]],
        time_column: str,
        target_column: str,
    ) -> list[dict[str, object]]:
        """
        Prepare historical rows for prediction.

        Args:
            rows:
                Raw historical data.

            time_column:
                Column representing time.

            target_column:
                Column containing values to predict.

        Returns:
            Cleaned historical rows.
        """

        self._validate_input(
            rows=rows,
            time_column=time_column,
            target_column=target_column,
        )

        prepared_rows: list[dict[str, object]] = []

        for row in rows:

            prepared_row = self._prepare_row(
                row=row,
                time_column=time_column,
                target_column=target_column,
            )

            if prepared_row is not None:

                prepared_rows.append(
                    prepared_row,
                )

        if not prepared_rows:
            raise ValueError(
                "Aucune donnée historique valide "
                "n'est disponible pour la prédiction."
            )

        return prepared_rows

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
        Validate prediction input.
        """

        if not rows:
            raise ValueError(
                "Aucune donnée historique fournie."
            )

        if not time_column.strip():
            raise ValueError(
                "La colonne temporelle est obligatoire."
            )

        if not target_column.strip():
            raise ValueError(
                "La colonne cible est obligatoire."
            )

    # ==========================================================
    # ROW PREPARATION
    # ==========================================================

    @staticmethod
    def _prepare_row(
        *,
        row: dict[str, object],
        time_column: str,
        target_column: str,
    ) -> dict[str, object] | None:
        """
        Validate and prepare one historical row.
        """

        if (
            time_column not in row
            or target_column not in row
        ):
            return None

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
            return None

        prepared_row = dict(
            row,
        )

        return prepared_row