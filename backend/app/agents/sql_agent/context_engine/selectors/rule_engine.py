from __future__ import annotations

from app.agents.sql_agent.context_engine.selectors.rules import (
    Rule,
)

__all__ = ["RuleEngine"]


class RuleEngine:
    """
    Evaluate business rules against a user question.

    Responsibilities
    ----------------
    - Normalize the user question.
    - Evaluate all available rules.
    - Return the activated rules.
    """

    def __init__(
        self,
        rules: list[Rule],
    ) -> None:
        self.rules = rules

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def evaluate(
        self,
        question: str,
    ) -> list[Rule]:
        """
        Evaluate all business rules and return the activated ones.
        """

        normalized_question = self._normalize_question(
            question,
        )

        return [
            rule
            for rule in self.rules
            if self._matches_rule(
                normalized_question,
                rule,
            )
        ]

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _normalize_question(
        self,
        question: str,
    ) -> str:
        """
        Normalize the user question before rule evaluation.
        """

        return question.casefold()

    def _matches_rule(
        self,
        question: str,
        rule: Rule,
    ) -> bool:
        """
        Return True if at least one rule keyword matches the question.
        """

        return any(
            keyword.casefold() in question
            for keyword in rule.keywords
        )