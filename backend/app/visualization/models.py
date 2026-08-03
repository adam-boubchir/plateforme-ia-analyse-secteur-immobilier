from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

# ==========================================================
# Type aliases
# ==========================================================

Row = Mapping[str, Any]
Rows = Sequence[Row]


# ==========================================================
# Enumerations
# ==========================================================

class ChartType(str, Enum):
    """Supported visualization types."""

    BAR = "bar"
    HORIZONTAL_BAR = "horizontal_bar"
    LINE = "line"
    AREA = "area"
    PIE = "pie"
    DONUT = "donut"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    MAP = "map"
    TABLE = "table"
    KPI_CARD = "kpi_card"


class VisualizationIntent(str, Enum):
    """Business intent detected from the user's request."""

    COMPARISON = "comparison"
    TREND = "trend"
    DISTRIBUTION = "distribution"
    RANKING = "ranking"
    CORRELATION = "correlation"
    GEOGRAPHIC = "geographic"
    COMPOSITION = "composition"
    EVOLUTION = "evolution"
    SUMMARY = "summary"
    UNKNOWN = "unknown"


# ==========================================================
# Generic visualization metadata
# ==========================================================

@dataclass(slots=True)
class DatasetInfo:
    """
    Generic dataset information used by the visualization engine.

    This class intentionally stays independent from the Report Agent
    so that the visualization engine can be reused by other agents.
    """

    categorical_columns: list[str] = field(default_factory=list)
    numeric_columns: list[str] = field(default_factory=list)
    datetime_columns: list[str] = field(default_factory=list)
    geographic_columns: list[str] = field(default_factory=list)


@dataclass(slots=True)
class StatisticsInfo:
    """
    Generic statistical information produced by any analysis engine.
    """

    statistics: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Scoring
# ==========================================================

@dataclass(slots=True)
class ChartScore:
    """
    Score assigned to a chart candidate.
    """

    chart_type: ChartType
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)


# ==========================================================
# Recommendation
# ==========================================================

@dataclass(slots=True, frozen=True)
class ChartRecommendation:
    """
    Final visualization recommendation returned by the engine.
    """

    chart_type: ChartType

    title: str

    x_axis: str | None

    y_axis: str | None

    score: float

    reasons: tuple[str, ...]


# ==========================================================
# Shared Context
# ==========================================================

@dataclass(slots=True)
class VisualizationContext:
    """
    Shared context exchanged between visualization components.
    """

    question: str

    rows: Rows

    dataset: DatasetInfo

    statistics: StatisticsInfo

    intent: VisualizationIntent = VisualizationIntent.UNKNOWN


__all__ = [
    "Row",
    "Rows",
    "ChartType",
    "VisualizationIntent",
    "DatasetInfo",
    "StatisticsInfo",
    "ChartScore",
    "ChartRecommendation",
    "VisualizationContext",
]