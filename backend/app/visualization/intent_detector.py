from __future__ import annotations

import re
import unicodedata

from app.visualization.models import (
    VisualizationContext,
    VisualizationIntent,
)


class IntentDetector:
    """
    Detect the dominant visualization intent from a natural language question.

    The detector is intentionally rule-based to provide deterministic,
    explainable and reproducible behavior. The implementation is designed
    so that a future NLP or LLM classifier can replace the matching logic
    without changing the public API.
    """

    _KEYWORDS: dict[
        VisualizationIntent,
        frozenset[str],
    ] = {
        VisualizationIntent.COMPARISON: frozenset({
            "compare",
            "comparaison",
            "comparer",
            "versus",
            "vs",
            "difference",
        }),

        VisualizationIntent.TREND: frozenset({
            "evolution",
            "trend",
            "historique",
            "croissance",
            "diminution",
            "progression",
        }),

        VisualizationIntent.DISTRIBUTION: frozenset({
            "distribution",
            "repartition",
            "part",
            "pourcentage",
            "share",
        }),

        VisualizationIntent.RANKING: frozenset({
            "top",
            "classement",
            "highest",
            "lowest",
            "maximum",
            "minimum",
        }),

        VisualizationIntent.GEOGRAPHIC: frozenset({
            "region",
            "province",
            "ville",
            "commune",
            "carte",
            "map",
            "territoire",
        }),

        VisualizationIntent.CORRELATION: frozenset({
            "correlation",
            "relation",
            "impact",
            "influence",
        }),

        VisualizationIntent.COMPOSITION: frozenset({
            "composition",
            "structure",
            "breakdown",
        }),

        VisualizationIntent.SUMMARY: frozenset({
            "resume",
            "summary",
            "synthese",
            "overview",
        }),
    }

    def detect(
        self,
        context: VisualizationContext,
    ) -> VisualizationIntent:
        """
        Detect the dominant visualization intent.
        """

        words = set(self._normalize(context.question).split())

        for intent, keywords in self._KEYWORDS.items():
            if words & keywords:
                return intent

        return VisualizationIntent.UNKNOWN

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize a question before keyword matching.
        """

        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

        text = text.lower()

        text = re.sub(r"[^\w\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()


__all__ = [
    "IntentDetector",
]