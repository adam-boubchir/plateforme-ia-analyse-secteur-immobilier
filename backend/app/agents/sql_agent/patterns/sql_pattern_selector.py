from app.agents.sql_agent.patterns.sql_pattern_repository import (
    SQLPatternRepository,
)


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

    # =====================================================
    # PUBLIC
    # =====================================================

    def select(
        self,
        question: str,
        selection: dict,
    ) -> list[dict]:
        """
        Return the SQL patterns ordered by relevance.
        """

        question = question.lower()

        selected_patterns = []

        for pattern in self.repository.get_all_patterns():

            score = self._compute_score(

                question=question,

                pattern=pattern,

                selection=selection,

            )

            if score <= 0:
                continue

            selected_patterns.append(

                {
                    "score": score,
                    "pattern": pattern,
                }

            )

        selected_patterns.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return selected_patterns

    # =====================================================
    # PRIVATE
    # =====================================================

    def _compute_score(
        self,
        question: str,
        pattern: dict,
        selection: dict,
    ) -> int:
        """
        Compute the relevance score of one SQL pattern.
        """

        score = 0

        # -----------------------------------------
        # Intent keywords
        # -----------------------------------------

        for keyword in pattern.get(
            "intent",
            [],
        ):

            if keyword.lower() in question:

                score += 10

        # -----------------------------------------
        # SQL keywords
        # -----------------------------------------

        for keyword in pattern.get(
            "keywords",
            [],
        ):

            if keyword.lower() in question:

                score += 5

        # -----------------------------------------
        # Category detected by Knowledge Selector
        # -----------------------------------------

        detected_patterns = selection.get(
            "sql_patterns",
            [],
        )

        category = pattern.get(
            "category",
            "",
        )

        category_mapping = {

            "Aggregate": "Aggregate",

            "Ranking": "Ranking",

            "Comparison": "Comparison",

            "Evolution": "Evolution",

            "Geographic": "Geographic",

            "Statistics": "Statistics",

        }

        if (
            category_mapping.get(category)
            in detected_patterns
        ):

            score += 50

        # -----------------------------------------
        # Geographic bonus
        # -----------------------------------------

        if (
            selection.get("geographic")
            and category == "Geographic"
        ):

            score += 20

        # -----------------------------------------
        # Time-series bonus
        # -----------------------------------------

        if (
            selection.get("time_series")
            and category == "Evolution"
        ):

            score += 20

        # -----------------------------------------
        # Aggregation bonus
        # -----------------------------------------

        if (
            selection.get("aggregation")
            and category in (
                "Aggregate",
                "Statistics",
            )
        ):

            score += 15

        # -----------------------------------------
        # Join bonus
        # -----------------------------------------

        if (
            selection.get("needs_join")
            and category == "Geographic"
        ):

            score += 10

        return score