from __future__ import annotations

from pathlib import Path
from uuid import uuid4
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from reportlab.lib.units import cm

from app.pdf.pdf_models import PDFImage


__all__ = (
    "ChartGenerator",
)


class ChartGenerator:
    """
    Generate professional and context-aware charts from SQL results.

    Responsibilities
    ----------------
    - Detect temporal, categorical and numerical columns.
    - Identify relevant analytical measures.
    - Choose an appropriate chart type.
    - Aggregate duplicated categories when necessary.
    - Generate readable charts for PDF reports.
    - Avoid meaningless visualizations.
    - Save high-resolution PNG files.
    - Return PDFImage objects.

    Supported charts
    ----------------
    - Line chart     : temporal evolution.
    - Bar chart      : categorical comparison / ranking.
    - Pie chart      : meaningful part-to-whole composition.
    """

    # ==========================================================
    # CONFIGURATION
    # ==========================================================

    MAX_CATEGORIES_BAR = 15

    MAX_CATEGORIES_PIE = 6

    MIN_CATEGORIES_PIE = 2

    MAX_LINE_POINTS = 100

    FIGURE_DPI = 300

    BAR_FIGURE_SIZE = (11, 6)

    LINE_FIGURE_SIZE = (11, 6)

    PIE_FIGURE_SIZE = (8, 7)

    # Numeric columns that generally represent dimensions
    # rather than analytical measurements.
    IGNORED_NUMERIC_KEYWORDS = (
        "id",
        "code",
        "annee",
        "année",
        "year",
        "mois",
        "month",
        "jour",
        "day",
        "latitude",
        "longitude",
        "lat",
        "lon",
        "index",
    )

    # Words suggesting an analytical measurement.
    MEASURE_KEYWORDS = (
        "prix",
        "price",
        "montant",
        "amount",
        "cout",
        "coût",
        "cost",
        "valeur",
        "value",
        "loyer",
        "rent",
        "salaire",
        "revenu",
        "revenue",
        "taux",
        "rate",
        "pourcentage",
        "percentage",
        "quantite",
        "quantité",
        "quantity",
        "volume",
        "consommation",
        "consumption",
        "surface",
        "superficie",
        "population",
        "nombre",
        "count",
        "total",
        "moyenne",
        "average",
        "montant",
        "part",
        "share",
    )

    # Temporal column names.
    TEMPORAL_KEYWORDS = (
        "annee",
        "année",
        "year",
        "date",
        "datetime",
        "timestamp",
        "mois",
        "month",
        "periode",
        "période",
    )

    # Categorical columns that usually make good chart dimensions.
    CATEGORY_KEYWORDS = (
        "region",
        "région",
        "ville",
        "city",
        "province",
        "prefecture",
        "préfecture",
        "commune",
        "zone",
        "type",
        "produit",
        "product",
        "materiau",
        "matériau",
        "material",
        "activite",
        "activité",
        "secteur",
        "segment",
        "categorie",
        "catégorie",
        "agglomeration",
        "agglomération",
    )

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(
        self,
        *,
        output_directory: Path,
    ) -> None:

        self._output_directory = output_directory

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Do not rely on matplotlib global style.
        # We define the important visual properties ourselves.
        plt.rcParams.update(
            {
                "font.family": "DejaVu Sans",
                "axes.titlesize": 16,
                "axes.labelsize": 10,
                "xtick.labelsize": 9,
                "ytick.labelsize": 9,
                "figure.dpi": 120,
            }
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        rows: list[dict],
    ) -> list[PDFImage]:
        """
        Generate the most relevant chart(s) for the dataset.

        The generator intentionally does NOT create every possible
        chart. It chooses visualizations according to the structure
        of the returned SQL data.
        """

        if not rows:
            return []

        normalized_rows = self._normalize_rows(
            rows,
        )

        if not normalized_rows:
            return []

        temporal_column = (
            self._detect_temporal_column(
                normalized_rows,
            )
        )

        numeric_columns = (
            self._numeric_columns(
                normalized_rows,
            )
        )

        categorical_columns = (
            self._categorical_columns(
                normalized_rows,
            )
        )

        measure_column = (
            self._select_measure_column(
                rows=normalized_rows,
                numeric_columns=numeric_columns,
            )
        )

        if measure_column is None:
            return []

        images: list[PDFImage] = []

        # ------------------------------------------------------
        # 1. TEMPORAL DATA → LINE CHART
        # ------------------------------------------------------

        if temporal_column is not None:

            image = self._generate_line_chart(
                rows=normalized_rows,
                x_column=temporal_column,
                value_column=measure_column,
            )

            if image is not None:
                images.append(image)

                # A temporal evolution is usually best
                # represented by one clear chart.
                return images

        # ------------------------------------------------------
        # 2. CATEGORICAL DATA → BAR CHART
        # ------------------------------------------------------

        category_column = (
            self._select_category_column(
                rows=normalized_rows,
                categorical_columns=categorical_columns,
            )
        )

        if category_column is not None:

            image = self._generate_bar_chart(
                rows=normalized_rows,
                category_column=category_column,
                value_column=measure_column,
            )

            if image is not None:
                images.append(image)

        # ------------------------------------------------------
        # 3. PIE CHART
        # ------------------------------------------------------

        # Only create a pie chart when the dataset really looks
        # like a part-to-whole composition.
        if (
            category_column is not None
            and self._is_good_pie_candidate(
                rows=normalized_rows,
                category_column=category_column,
                value_column=measure_column,
            )
        ):

            image = self._generate_pie_chart(
                rows=normalized_rows,
                category_column=category_column,
                value_column=measure_column,
            )

            if image is not None:
                images.append(image)

        return images

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def _normalize_rows(
        self,
        rows: list[dict],
    ) -> list[dict]:
        """
        Remove empty rows and normalize dictionary structure.
        """

        normalized: list[dict] = []

        for row in rows:

            if not isinstance(row, dict):
                continue

            cleaned = {
                str(key): value
                for key, value in row.items()
            }

            if cleaned:
                normalized.append(
                    cleaned,
                )

        return normalized

    # ==========================================================
    # COLUMN DETECTION
    # ==========================================================

    def _numeric_columns(
        self,
        rows: list[dict],
    ) -> list[str]:
        """
        Detect columns containing numeric values.
        """

        if not rows:
            return []

        columns = list(
            rows[0].keys()
        )

        result: list[str] = []

        for column in columns:

            values = [
                row.get(column)
                for row in rows
                if row.get(column) is not None
            ]

            if not values:
                continue

            valid_numeric = all(
                isinstance(
                    value,
                    (int, float),
                )
                and not isinstance(
                    value,
                    bool,
                )
                for value in values
            )

            if valid_numeric:
                result.append(
                    column,
                )

        return result

    def _categorical_columns(
        self,
        rows: list[dict],
    ) -> list[str]:
        """
        Detect string-based categorical columns.
        """

        if not rows:
            return []

        columns = list(
            rows[0].keys()
        )

        result: list[str] = []

        for column in columns:

            values = [
                row.get(column)
                for row in rows
                if row.get(column) is not None
            ]

            if not values:
                continue

            if all(
                isinstance(
                    value,
                    str,
                )
                for value in values
            ):
                result.append(
                    column,
                )

        return result

    # ==========================================================
    # TEMPORAL DETECTION
    # ==========================================================

    def _detect_temporal_column(
        self,
        rows: list[dict],
    ) -> str | None:
        """
        Detect the most likely temporal column.

        Preference is given to columns whose names explicitly
        indicate year/date/month/period.
        """

        if not rows:
            return None

        columns = list(
            rows[0].keys()
        )

        candidates: list[
            tuple[str, int]
        ] = []

        for column in columns:

            column_lower = (
                column.strip().lower()
            )

            score = 0

            for keyword in self.TEMPORAL_KEYWORDS:

                if keyword in column_lower:
                    score += 10

            values = [
                row.get(column)
                for row in rows
                if row.get(column) is not None
            ]

            if not values:
                continue

            # Numeric years such as 2015, 2016, 2017.
            if all(
                isinstance(
                    value,
                    (int, float),
                )
                and not isinstance(
                    value,
                    bool,
                )
                for value in values
            ):
                year_like = all(
                    1900 <= float(value) <= 2100
                    for value in values
                )

                if year_like:
                    score += 15

            # Date-like strings.
            if all(
                isinstance(
                    value,
                    str,
                )
                for value in values
            ):
                if self._looks_like_date_values(
                    values,
                ):
                    score += 15

            if score > 0:
                candidates.append(
                    (
                        column,
                        score,
                    )
                )

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return candidates[0][0]

    def _looks_like_date_values(
        self,
        values: list[Any],
    ) -> bool:
        """
        Basic date detection without external dependencies.
        """

        if not values:
            return False

        detected = 0

        for value in values[:20]:

            text = str(value).strip()

            if (
                "-" in text
                or "/" in text
            ):
                detected += 1

        return detected >= max(
            1,
            min(
                len(values[:20]),
                3,
            ),
        )

    # ==========================================================
    # MEASURE SELECTION
    # ==========================================================

    def _select_measure_column(
        self,
        *,
        rows: list[dict],
        numeric_columns: list[str],
    ) -> str | None:
        """
        Select the most meaningful numerical measure.
        """

        if not numeric_columns:
            return None

        candidates: list[
            tuple[str, int, int]
        ] = []

        for column in numeric_columns:

            column_lower = (
                column.strip().lower()
            )

            # Ignore technical dimensions.
            if any(
                keyword in column_lower
                for keyword
                in self.IGNORED_NUMERIC_KEYWORDS
            ):
                continue

            score = 0

            for keyword in self.MEASURE_KEYWORDS:

                if keyword in column_lower:
                    score += 10

            values = [
                row.get(column)
                for row in rows
                if row.get(column) is not None
            ]

            candidates.append(
                (
                    column,
                    score,
                    len(values),
                )
            )

        if not candidates:

            # If every numeric column was ignored,
            # use the first numeric column as a fallback.
            return numeric_columns[0]

        candidates.sort(
            key=lambda item: (
                item[1],
                item[2],
            ),
            reverse=True,
        )

        return candidates[0][0]

    # ==========================================================
    # CATEGORY SELECTION
    # ==========================================================

    def _select_category_column(
        self,
        *,
        rows: list[dict],
        categorical_columns: list[str],
    ) -> str | None:
        """
        Select the most useful categorical dimension.
        """

        if not categorical_columns:
            return None

        candidates: list[
            tuple[str, int, int]
        ] = []

        for column in categorical_columns:

            column_lower = (
                column.strip().lower()
            )

            unique_count = len(
                {
                    str(
                        row.get(column)
                    )
                    for row in rows
                    if row.get(column) is not None
                }
            )

            if unique_count < 2:
                continue

            score = 0

            for keyword in self.CATEGORY_KEYWORDS:

                if keyword in column_lower:
                    score += 10

            # Prefer dimensions with a reasonable number
            # of categories.
            if unique_count <= self.MAX_CATEGORIES_BAR:
                score += 5

            candidates.append(
                (
                    column,
                    score,
                    unique_count,
                )
            )

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: (
                item[1],
                -item[2],
            ),
            reverse=True,
        )

        return candidates[0][0]

    # ==========================================================
    # BAR CHART
    # ==========================================================

    def _generate_bar_chart(
        self,
        *,
        rows: list[dict],
        category_column: str,
        value_column: str,
    ) -> PDFImage | None:
        """
        Generate a ranked categorical comparison.

        Duplicate categories are aggregated by mean.
        """

        aggregated = self._aggregate_by_category(
            rows=rows,
            category_column=category_column,
            value_column=value_column,
        )

        if not aggregated:
            return None

        # Keep the chart readable.
        aggregated = aggregated[
            : self.MAX_CATEGORIES_BAR
        ]

        labels = [
            item[0]
            for item in aggregated
        ]

        values = [
            item[1]
            for item in aggregated
        ]

        horizontal = (
            len(labels) >= 6
        )

        figure, axis = plt.subplots(
            figsize=self.BAR_FIGURE_SIZE,
        )

        if horizontal:

            labels = labels[::-1]
            values = values[::-1]

            bars = axis.barh(
                labels,
                values,
                height=0.62,
            )

        else:

            bars = axis.bar(
                labels,
                values,
                width=0.62,
            )

            axis.tick_params(
                axis="x",
                rotation=30,
            )

        axis.set_title(
            self._chart_title(
                value_column=value_column,
                category_column=category_column,
                chart_type="bar",
            ),
            fontweight="bold",
            pad=15,
        )

        axis.set_xlabel(
            self._humanize_label(
                category_column,
            )
            if not horizontal
            else "",
        )

        axis.set_ylabel(
            self._humanize_label(
                value_column,
            )
            if horizontal
            else self._humanize_label(
                value_column,
            ),
        )

        axis.grid(
            axis="y"
            if not horizontal
            else "x",
            alpha=0.25,
        )

        axis.set_axisbelow(True)

        self._format_axis_values(
            axis=axis,
            horizontal=horizontal,
        )

        self._add_bar_labels(
            axis=axis,
            bars=bars,
            horizontal=horizontal,
        )

        figure.tight_layout()

        output_path = self._save_figure(
            figure=figure,
            prefix="bar",
            value_column=value_column,
        )

        plt.close(figure)

        return PDFImage(
            path=str(output_path),
            caption=(
                f"Comparaison de "
                f"{self._humanize_label(value_column)} "
                f"selon "
                f"{self._humanize_label(category_column)}."
            ),
            width=16 * cm,
        )

    # ==========================================================
    # LINE CHART
    # ==========================================================

    def _generate_line_chart(
        self,
        *,
        rows: list[dict],
        x_column: str,
        value_column: str,
    ) -> PDFImage | None:
        """
        Generate a readable temporal evolution chart.

        Multiple SQL rows belonging to the same temporal period
        are aggregated into one representative value.

        Median is used to reduce the influence of outliers.
        """

        aggregated = self._aggregate_temporal_data(
            rows=rows,
            temporal_column=x_column,
            value_column=value_column,
        )

        if len(aggregated) < 2:
            return None

        x_values = [
            item[0]
            for item in aggregated
        ]

        y_values = [
            item[1]
            for item in aggregated
        ]

        figure, axis = plt.subplots(
            figsize=(11, 6),
        )

        # ------------------------------------------------------
        # LINE
        # ------------------------------------------------------

        axis.plot(
            range(len(y_values)),
            y_values,
            linewidth=2.5,
            marker="o",
            markersize=6,
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        axis.set_title(
            (
                f"Évolution de la médiane de "
                f"{self._humanize_label(value_column)} "
                f"par {self._humanize_label(x_column)}"
            ),
            fontweight="bold",
            fontsize=16,
            pad=18,
        )

        # ------------------------------------------------------
        # AXES
        # ------------------------------------------------------

        axis.set_xlabel(
            self._humanize_label(
                x_column,
            ),
            fontsize=10,
        )

        axis.set_ylabel(
            f"Médiane de "
            f"{self._humanize_label(value_column)}",
            fontsize=10,
        )

        # ------------------------------------------------------
        # X AXIS
        # ------------------------------------------------------

        positions = list(
            range(
                len(x_values),
            )
        )

        axis.set_xticks(
            positions,
        )

        axis.set_xticklabels(
            x_values,
            rotation=0,
            ha="center",
        )

        # ------------------------------------------------------
        # GRID
        # ------------------------------------------------------

        axis.grid(
            axis="y",
            alpha=0.25,
        )

        axis.set_axisbelow(
            True,
        )

        # ------------------------------------------------------
        # Y AXIS
        # ------------------------------------------------------

        axis.yaxis.set_major_formatter(
            FuncFormatter(
                lambda value, _: (
                    self._format_axis_number(
                        value,
                    )
                )
            )
        )

        # ------------------------------------------------------
        # VALUE LABELS
        # ------------------------------------------------------

        for index, value in enumerate(
            y_values,
        ):

            axis.annotate(
                self._format_axis_number(
                    value,
                ),
                xy=(
                    index,
                    value,
                ),
                xytext=(
                    0,
                    8,
                ),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                fontweight="bold",
            )

        # ------------------------------------------------------
        # LIMITS
        # ------------------------------------------------------

        axis.margins(
            x=0.03,
            y=0.15,
        )

        # ------------------------------------------------------
        # SAVE
        # ------------------------------------------------------

        figure.tight_layout()

        output_path = self._save_figure(
            figure=figure,
            prefix="line",
            value_column=value_column,
        )

        plt.close(
            figure,
        )

        return PDFImage(
            path=str(output_path),
            caption=(
                f"Évolution annuelle de la médiane de "
                f"{self._humanize_label(value_column)} "
                f"sur la période étudiée."
            ),
            width=16 * cm,
        )
    # ==========================================================
    # PIE CHART
    # ==========================================================

    def _generate_pie_chart(
        self,
        *,
        rows: list[dict],
        category_column: str,
        value_column: str,
    ) -> PDFImage | None:
        """
        Generate a part-to-whole composition chart.
        """

        aggregated = self._aggregate_by_category(
            rows=rows,
            category_column=category_column,
            value_column=value_column,
        )

        if not aggregated:
            return None

        aggregated = aggregated[
            : self.MAX_CATEGORIES_PIE
        ]

        labels = [
            item[0]
            for item in aggregated
        ]

        values = [
            item[1]
            for item in aggregated
        ]

        if any(
            value < 0
            for value in values
        ):
            return None

        total = sum(values)

        if total <= 0:
            return None

        figure, axis = plt.subplots(
            figsize=self.PIE_FIGURE_SIZE,
        )

        wedges, _, autotexts = axis.pie(
            values,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.72,
            wedgeprops={
                "linewidth": 1,
                "edgecolor": "white",
            },
        )

        for text in autotexts:
            text.set_fontsize(9)
            text.set_fontweight("bold")

        axis.legend(
            wedges,
            labels,
            title=self._humanize_label(
                category_column,
            ),
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=8,
        )

        axis.set_title(
            (
                "Répartition de "
                f"{self._humanize_label(value_column)}"
            ),
            fontweight="bold",
            pad=15,
        )

        axis.axis("equal")

        figure.tight_layout()

        output_path = self._save_figure(
            figure=figure,
            prefix="pie",
            value_column=value_column,
        )

        plt.close(figure)

        return PDFImage(
            path=str(output_path),
            caption=(
                f"Répartition de "
                f"{self._humanize_label(value_column)} "
                f"par "
                f"{self._humanize_label(category_column)}."
            ),
            width=14 * cm,
        )

    # ==========================================================
    # AGGREGATION
    # ==========================================================

    def _aggregate_by_category(
        self,
        *,
        rows: list[dict],
        category_column: str,
        value_column: str,
    ) -> list[tuple[str, float]]:
        """
        Aggregate values by category using the mean.

        Example:
            Rabat -> 80
            Rabat -> 90
            Casablanca -> 100

        becomes:

            Rabat -> 85
            Casablanca -> 100
        """

        grouped: dict[
            str,
            list[float]
        ] = {}

        for row in rows:

            category = row.get(
                category_column,
            )

            value = self._to_float(
                row.get(
                    value_column,
                ),
            )

            if category is None:
                continue

            if value is None:
                continue

            key = str(
                category,
            )

            grouped.setdefault(
                key,
                [],
            ).append(
                value,
            )

        result = [
            (
                category,
                sum(values) / len(values),
            )
            for category, values
            in grouped.items()
            if values
        ]

        # Highest values first.
        result.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return result

    # ==========================================================
    # PIE CANDIDATE
    # ==========================================================

    def _is_good_pie_candidate(
        self,
        *,
        rows: list[dict],
        category_column: str,
        value_column: str,
    ) -> bool:
        """
        Determine whether a pie chart is meaningful.

        Pie charts are intentionally restricted to small,
        non-negative categorical datasets.
        """

        aggregated = self._aggregate_by_category(
            rows=rows,
            category_column=category_column,
            value_column=value_column,
        )

        if not (
            self.MIN_CATEGORIES_PIE
            <= len(aggregated)
            <= self.MAX_CATEGORIES_PIE
        ):
            return False

        values = [
            item[1]
            for item in aggregated
        ]

        if any(
            value < 0
            for value in values
        ):
            return False

        if sum(values) <= 0:
            return False

        # If one category dominates almost everything,
        # a pie chart provides little value.
        total = sum(values)

        largest_share = (
            max(values)
            / total
        )

        if largest_share > 0.90:
            return False

        return True

    # ==========================================================
    # VISUAL HELPERS
    # ==========================================================

    def _add_bar_labels(
        self,
        *,
        axis,
        bars,
        horizontal: bool,
    ) -> None:
        """
        Display readable values on bars.
        """

        for bar in bars:

            if horizontal:

                value = bar.get_width()

                axis.annotate(
                    self._format_axis_number(
                        value,
                    ),
                    xy=(
                        value,
                        bar.get_y()
                        + bar.get_height()
                        / 2,
                    ),
                    xytext=(
                        5,
                        0,
                    ),
                    textcoords="offset points",
                    va="center",
                    fontsize=8,
                )

            else:

                value = bar.get_height()

                axis.annotate(
                    self._format_axis_number(
                        value,
                    ),
                    xy=(
                        bar.get_x()
                        + bar.get_width()
                        / 2,
                        value,
                    ),
                    xytext=(
                        0,
                        5,
                    ),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )

    def _add_line_annotations(
        self,
        *,
        axis,
        x_values,
        y_values,
    ) -> None:
        """
        Annotate the first and last values.
        """

        if not y_values:
            return

        if len(y_values) == 1:
            indices = [0]
        else:
            indices = [
                0,
                len(y_values) - 1,
            ]

        for index in indices:

            axis.annotate(
                self._format_axis_number(
                    y_values[index],
                ),
                xy=(
                    index,
                    y_values[index],
                ),
                xytext=(
                    0,
                    8,
                ),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                fontweight="bold",
            )

    def _format_axis_values(
        self,
        *,
        axis,
        horizontal: bool,
    ) -> None:
        """
        Format numerical axis values.
        """

        target_axis = (
            axis.xaxis
            if horizontal
            else axis.yaxis
        )

        target_axis.set_major_formatter(
            FuncFormatter(
                lambda value, _: (
                    self._format_axis_number(
                        value,
                    )
                )
            )
        )

    # ==========================================================
    # LABELS / TITLES
    # ==========================================================

    def _humanize_label(
        self,
        label: str,
    ) -> str:
        """
        Convert technical database column names into
        readable labels.

        Example:
            prix_moyen_m2
            →
            Prix moyen m2
        """

        text = str(label)

        text = text.replace(
            "_",
            " ",
        )

        text = text.replace(
            "-",
            " ",
        )

        return text.strip().capitalize()

    def _chart_title(
        self,
        *,
        value_column: str,
        category_column: str,
        chart_type: str,
    ) -> str:
        """
        Build a professional chart title.
        """

        value = self._humanize_label(
            value_column,
        )

        category = self._humanize_label(
            category_column,
        )

        if chart_type == "line":

            return (
                f"Évolution de {value}"
                f" selon {category}"
            )

        return (
            f"{value} par {category}"
        )

    # ==========================================================
    # TEMPORAL HELPERS
    # ==========================================================

    def _temporal_sort_key(
        self,
        value: Any,
    ) -> Any:
        """
        Produce a stable sorting key for years/dates.
        """

        if isinstance(
            value,
            (int, float),
        ):
            return float(value)

        text = str(value).strip()

        # YYYY-MM-DD / YYYY-MM / YYYY
        if len(text) >= 4:

            prefix = text[:4]

            if prefix.isdigit():
                return (
                    int(prefix),
                    text,
                )

        return text

    def _format_temporal_label(
        self,
        value: Any,
    ) -> str:
        """
        Format temporal values for chart axes.
        """

        if isinstance(
            value,
            float,
        ):
            if value.is_integer():
                return str(
                    int(value),
                )

        return str(value)

    # ==========================================================
    # NUMBER HELPERS
    # ==========================================================

    def _to_float(
        self,
        value: Any,
    ) -> float | None:
        """
        Safely convert a value to float.
        """

        if value is None:
            return None

        if isinstance(
            value,
            bool,
        ):
            return None

        try:
            return float(
                value,
            )

        except (
            TypeError,
            ValueError,
        ):
            return None

    def _format_axis_number(
        self,
        value: float,
    ) -> str:
        """
        Format numbers in a compact French-friendly way.
        """

        if abs(value) >= 1_000_000:
            return (
                f"{value / 1_000_000:.1f} M"
            )

        if abs(value) >= 1_000:
            return (
                f"{value / 1_000:.1f} k"
            )

        if float(value).is_integer():
            return str(
                int(value),
            )

        return (
            f"{value:.1f}"
        )

    # ==========================================================
    # FILE OUTPUT
    # ==========================================================

    def _save_figure(
        self,
        *,
        figure,
        prefix: str,
        value_column: str,
    ) -> Path:
        """
        Save a matplotlib figure as a high-resolution PNG.
        """

        safe_value = (
            self._safe_filename(
                value_column,
            )
        )

        output_path = (
            self._output_directory
            / (
                f"{prefix}_"
                f"{safe_value}_"
                f"{uuid4().hex}.png"
            )
        )

        figure.savefig(
            output_path,
            dpi=self.FIGURE_DPI,
            bbox_inches="tight",
            facecolor="white",
        )

        return output_path

    def _safe_filename(
        self,
        value: str,
    ) -> str:
        """
        Make a column name safe for filenames.
        """

        return "".join(
            character
            if character.isalnum()
            else "_"
            for character in str(value)
        ).strip(
            "_",
        )[:80]

    def _aggregate_temporal_data(
        self,
        *,
        rows: list[dict],
        temporal_column: str,
        value_column: str,
    ) -> list[tuple[str, float]]:
        """
        Aggregate numerical values by temporal period.

        For temporal analysis, the median is used because it is
        more robust to extreme values and outliers than the mean.
        """

        grouped: dict[str, list[float]] = {}

        for row in rows:

            raw_period = row.get(
                temporal_column,
            )

            raw_value = row.get(
                value_column,
            )

            if raw_period is None:
                continue

            numeric_value = self._to_float(
                raw_value,
            )

            if numeric_value is None:
                continue

            period = self._format_temporal_label(
                raw_period,
            )

            grouped.setdefault(
                period,
                [],
            ).append(
                numeric_value,
            )

        result: list[
            tuple[str, float]
        ] = []

        for period, values in grouped.items():

            if not values:
                continue

            ordered = sorted(
                values,
            )

            middle = len(ordered) // 2

            if len(ordered) % 2 == 0:

                median = (
                    ordered[middle - 1]
                    + ordered[middle]
                ) / 2

            else:

                median = ordered[middle]

            result.append(
                (
                    period,
                    median,
                )
            )

        result.sort(
            key=lambda item: self._temporal_sort_key(
                item[0],
            )
        )

        return result