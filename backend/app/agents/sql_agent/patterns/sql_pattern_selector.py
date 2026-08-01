from app.agents.sql_agent.patterns.sql_pattern_repository import (
    SQLPatternRepository,
)

# ==========================================================
# CONSTANTS
# ==========================================================

CATEGORY_MAPPING = {
    "Aggregate": "Aggregate",
    "Ranking": "Ranking",
    "Comparison": "Comparison",
    "Evolution": "Evolution",
    "Geographic": "Geographic",
    "Statistics": "Statistics",
}


class SQLPatternSelector:
    """
    Select the SQL patterns that best match the
    user's question and the detected business context.
    """

    def __init__(
        self,
        repository: SQLPatternRepository,
    ):
        self.repository = repository

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        question: str,
        selection: dict,
    ) -> list[dict]:
        """
        Return SQL patterns ordered by relevance.
        """

        question = self._normalize_question(
            question,
        )

        patterns = []

        for pattern in self.repository.get_all_patterns():

            score = self._compute_score(
                question=question,
                pattern=pattern,
                selection=selection,
            )

            if score <= 0:
                continue

            patterns.append(
                {
                    "score": score,
                    "pattern": pattern,
                }
            )

        return sorted(
            patterns,
            key=lambda item: item["score"],
            reverse=True,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _normalize_question(
        self,
        question: str,
    ) -> str:
        """
        Normalize the user question before pattern matching.
        """

        return question.lower()

    def _compute_score(
        self,
        question: str,
        pattern: dict,
        selection: dict,
    ) -> int:
        """
        Compute the total relevance score of one SQL pattern.
        """

        score = self._compute_keyword_score(
            question,
            pattern,
        )

        score += self._compute_category_bonus(
            pattern,
            selection,
        )

        score += self._compute_context_bonus(
            pattern,
            selection,
        )

        return score

    def _compute_keyword_score(
        self,
        question: str,
        pattern: dict,
    ) -> int:
        """
        Compute the score associated with keyword matches.
        """

        score = 0

        for keyword in pattern.get(
            "intent",
            [],
        ):

            if keyword.lower() in question:

                score += 10

        for keyword in pattern.get(
            "keywords",
            [],
        ):

            if keyword.lower() in question:

                score += 5

        return score

    def _compute_category_bonus(
        self,
        pattern: dict,
        selection: dict,
    ) -> int:
        """
        Bonus if the Knowledge Selector already detected
        this SQL category.
        """

        detected_patterns = selection.get(
            "sql_patterns",
            [],
        )

        category = pattern.get(
            "category",
            "",
        )

        if (
            CATEGORY_MAPPING.get(category)
            in detected_patterns
        ):
            return 50

        return 0

    def _compute_context_bonus(
        self,
        pattern: dict,
        selection: dict,
    ) -> int:
        """
        Compute contextual bonuses.
        """

        category = pattern.get(
            "category",
            "",
        )

        bonus = 0

        # Geographic bonus
        if (
            selection.get("geographic")
            and category == "Geographic"
        ):
            bonus += 20

        # Time-series bonus
        if (
            selection.get("time_series")
            and category == "Evolution"
        ):
            bonus += 20

        # Aggregation bonus
        if (
            selection.get("aggregation")
            and category in (
                "Aggregate",
                "Statistics",
            )
        ):
            bonus += 15

        # Join bonus
        if (
            selection.get("needs_join")
            and category == "Geographic"
        ):
            bonus += 10

        return bonus