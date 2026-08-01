from __future__ import annotations

from typing import Any

__all__ = ["FewShotProvider"]

# ==========================================================
# CONSTANTS
# ==========================================================

EXAMPLE_SEPARATOR = "=" * 60

NO_EXAMPLE_MESSAGE = "No example available."


class FewShotProvider:
    """
    Provide the most relevant few-shot examples for a question.

    The current implementation uses simple keyword matching.
    It can later be replaced by a semantic search engine
    without modifying the PromptBuilder.
    """

    def __init__(
        self,
        examples: list[dict[str, Any]],
    ) -> None:
        self.examples = examples

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get_examples(
        self,
        question: str,
        max_examples: int = 3,
    ) -> str:
        """
        Return the most relevant examples.
        """

        ranked_examples = self._rank_examples(
            question,
        )

        if not ranked_examples:
            return NO_EXAMPLE_MESSAGE

        formatted_examples: list[str] = []

        for example in ranked_examples[:max_examples]:
            formatted_examples.extend(
                self._format_example(
                    example,
                )
            )

        return "\n".join(formatted_examples)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _rank_examples(
        self,
        question: str,
    ) -> list[dict[str, Any]]:
        """
        Rank examples using keyword matching.

        This implementation can later be replaced
        by semantic vector search.
        """

        normalized_question = question.casefold()

        scored_examples: list[tuple[int, dict[str, Any]]] = []

        for example in self.examples:

            keywords = example.get(
                "keywords",
                [],
            )

            score = self._calculate_score(
                normalized_question,
                keywords,
            )

            scored_examples.append(
                (
                    score,
                    example,
                )
            )

        scored_examples.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            example
            for score, example in scored_examples
            if score > 0
        ]

    def _format_example(
        self,
        example: dict[str, Any],
    ) -> list[str]:
        """
        Format one few-shot example.
        """

        return [
            EXAMPLE_SEPARATOR,
            f"Question : {example.get('question', '')}",
            "",
            "SQL",
            example.get("sql", ""),
            EXAMPLE_SEPARATOR,
            "",
        ]

    def _calculate_score(
        self,
        question: str,
        keywords: list[str],
    ) -> int:
        """
        Compute a keyword relevance score.
        """

        score = 0

        for keyword in keywords:

            if keyword.casefold() in question:
                score += 1

        return score