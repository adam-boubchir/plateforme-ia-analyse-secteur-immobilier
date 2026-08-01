from app.agents.sql_agent.context_engine.selectors.rules import (
    Rule,
)


class RuleScorer:
    """
    Compute a relevance score for every activated rule.

    The score is intentionally simple so that it can
    easily evolve later with AI, embeddings or statistics.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def score(
        self,
        question: str,
        rules: list[Rule],
    ) -> list[tuple[Rule, int]]:
        """
        Returns the activated rules ordered by relevance.
        """

        question = self._normalize_question(
            question,
        )

        scored_rules = [
            (
                rule,
                self._compute_score(
                    question,
                    rule,
                ),
            )
            for rule in rules
        ]

        return sorted(
            scored_rules,
            key=lambda item: item[1],
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
        Normalize the user question before scoring.
        """

        return question.lower()

    def _compute_score(
        self,
        question: str,
        rule: Rule,
    ) -> int:
        """
        Compute one rule score.
        """

        score = self._compute_keyword_score(
            question,
            rule,
        )

        score += self._compute_bonus(
            rule,
        )

        return score

    def _compute_keyword_score(
        self,
        question: str,
        rule: Rule,
    ) -> int:
        """
        Compute the score associated with keyword matches.
        """

        score = 0

        for keyword in rule.keywords:

            if keyword.lower() in question:

                score += 10
                score += len(keyword) // 3

        return score

    def _compute_bonus(
        self,
        rule: Rule,
    ) -> int:
        """
        Compute structural bonuses.
        """

        bonus = 0

        if rule.needs_join:
            bonus += 2

        if rule.aggregation:
            bonus += 2

        if rule.geographic:
            bonus += 2

        if rule.time_series:
            bonus += 2

        return bonus