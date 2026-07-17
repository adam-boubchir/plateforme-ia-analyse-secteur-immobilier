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

        question = question.lower()

        scored_rules = []

        for rule in rules:

            score = self._compute_score(
                question,
                rule,
            )

            scored_rules.append(
                (
                    rule,
                    score,
                )
            )

        scored_rules.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return scored_rules

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _compute_score(
        self,
        question: str,
        rule: Rule,
    ) -> int:
        """
        Compute one rule score.
        """

        score = 0

        # -----------------------------------------
        # Keyword matches
        # -----------------------------------------

        for keyword in rule.keywords:

            if keyword.lower() in question:

                score += 10

                # Longer keywords are generally
                # more specific.
                score += len(keyword) // 3

        # -----------------------------------------
        # Join bonus
        # -----------------------------------------

        if rule.needs_join:

            score += 2

        # -----------------------------------------
        # Aggregation bonus
        # -----------------------------------------

        if rule.aggregation:

            score += 2

        # -----------------------------------------
        # Geographic bonus
        # -----------------------------------------

        if rule.geographic:

            score += 2

        # -----------------------------------------
        # Time-series bonus
        # -----------------------------------------

        if rule.time_series:

            score += 2

        return score

    # ==========================================================
    # DEBUG
    # ==========================================================

    def explain(
        self,
        question: str,
        rules: list[Rule],
    ) -> None:

        scored = self.score(
            question,
            rules,
        )

        print("\n" + "=" * 100)
        print("RULE SCORING")
        print("=" * 100)

        for rule, score in scored:

            print(f"{score:>3}  ->  {rule.name}")

        print("=" * 100)
        print()