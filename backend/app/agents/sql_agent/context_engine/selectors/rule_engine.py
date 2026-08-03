from __future__ import annotations

from app.agents.sql_agent.context_engine.selectors.rules import (
    Rule,
)

__all__ = ("RuleEngine",)


class RuleEngine:
    """
    Evaluate business rules against a user question.

    Responsibilities
    ----------------
    - Normalize the user question.
    - Evaluate every registered business rule.
    - Return the list of activated rules.
    """

    def __init__(
        self,
        *,
        rules: list[Rule],
    ) -> None:
        self._rules = rules

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def evaluate(
        self,
        *,
        question: str,
    ) -> list[Rule]:
        """
        Evaluate every business rule against a user question.

        Args:
            question:
                User natural-language question.

        Returns:
            List of activated business rules.
        """

        normalized_question = self._normalize_question(
            question=question,
        )

        activated_rules = [
            rule
            for rule in self._rules
            if self._matches_rule(
                question=normalized_question,
                rule=rule,
            )
        ]

        return activated_rules

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _normalize_question(
        *,
        question: str,
    ) -> str:
        """
        Normalize a user question before evaluating rules.

        Args:
            question:
                User question.

        Returns:
            Normalized question.
        """

        normalized_question = question.casefold().strip()

        return normalized_question

    @staticmethod
    def _matches_rule(
        *,
        question: str,
        rule: Rule,
    ) -> bool:
        """
        Determine whether a rule matches the user question.

        Args:
            question:
                Normalized user question.

            rule:
                Business rule.

        Returns:
            True if at least one keyword matches.
        """

        has_match = any(
            keyword.casefold() in question
            for keyword in rule.keywords
        )

        return has_match