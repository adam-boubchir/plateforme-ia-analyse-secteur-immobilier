from __future__ import annotations

from app.agents.sql_agent.context_engine.selectors.rules import (
    Rule,
)

__all__ = ("RuleScorer",)

# ==========================================================
# CONSTANTS
# ==========================================================

_KEYWORD_MATCH_SCORE = 10
_KEYWORD_LENGTH_DIVISOR = 3

_JOIN_BONUS = 2
_AGGREGATION_BONUS = 2
_GEOGRAPHIC_BONUS = 2
_TIME_SERIES_BONUS = 2


class RuleScorer:
    """
    Compute a relevance score for every activated business rule.

    Responsibilities
    ----------------
    - Normalize the user question.
    - Compute a relevance score for each activated rule.
    - Return the rules ordered by descending relevance.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def score(
        self,
        *,
        question: str,
        rules: list[Rule],
    ) -> list[tuple[Rule, int]]:
        """
        Compute the relevance score of every activated rule.

        Args:
            question:
                User natural-language question.

            rules:
                Activated business rules.

        Returns:
            List of tuples (Rule, Score) sorted by descending score.
        """

        normalized_question = self._normalize_question(
            question=question,
        )

        scored_rules = [
            (
                rule,
                self._compute_score(
                    question=normalized_question,
                    rule=rule,
                ),
            )
            for rule in rules
        ]

        sorted_rules = sorted(
            scored_rules,
            key=lambda item: item[1],
            reverse=True,
        )

        return sorted_rules

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _normalize_question(
        *,
        question: str,
    ) -> str:
        """
        Normalize the user question before scoring.

        Args:
            question:
                User question.

        Returns:
            Normalized question.
        """

        normalized_question = question.casefold().strip()

        return normalized_question

    @classmethod
    def _compute_score(
        cls,
        *,
        question: str,
        rule: Rule,
    ) -> int:
        """
        Compute the total relevance score of a business rule.

        Args:
            question:
                Normalized user question.

            rule:
                Business rule.

        Returns:
            Total relevance score.
        """

        keyword_score = cls._compute_keyword_score(
            question=question,
            rule=rule,
        )

        bonus_score = cls._compute_bonus(
            rule=rule,
        )

        total_score = (
            keyword_score
            + bonus_score
        )

        return total_score

    @classmethod
    def _compute_keyword_score(
        cls,
        *,
        question: str,
        rule: Rule,
    ) -> int:
        """
        Compute the score associated with keyword matches.

        Args:
            question:
                Normalized user question.

            rule:
                Business rule.

        Returns:
            Keyword relevance score.
        """

        score = 0

        for keyword in rule.keywords:

            if keyword.casefold() in question:

                score += _KEYWORD_MATCH_SCORE
                score += (
                    len(keyword)
                    // _KEYWORD_LENGTH_DIVISOR
                )

        return score

    @staticmethod
    def _compute_bonus(
        *,
        rule: Rule,
    ) -> int:
        """
        Compute structural bonuses associated with a business rule.

        Args:
            rule:
                Business rule.

        Returns:
            Structural bonus.
        """

        bonus = 0

        if rule.needs_join:
            bonus += _JOIN_BONUS

        if rule.aggregation:
            bonus += _AGGREGATION_BONUS

        if rule.geographic:
            bonus += _GEOGRAPHIC_BONUS

        if rule.time_series:
            bonus += _TIME_SERIES_BONUS

        return bonus