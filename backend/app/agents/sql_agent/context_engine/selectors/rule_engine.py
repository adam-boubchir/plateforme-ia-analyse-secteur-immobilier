from app.agents.sql_agent.context_engine.selectors.rules import (
    RULES,
    Rule,
)


class RuleEngine:
    """
    Rule engine responsible for matching a user question
    against all predefined business rules.

    It returns the list of activated rules.
    """

    def __init__(self):

        self.rules = RULES

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def evaluate(
        self,
        question: str,
    ) -> list[Rule]:
        """
        Evaluate every rule.

        Returns the activated rules.
        """

        question = question.lower()

        activated_rules = []

        for rule in self.rules:

            if self._match_rule(
                question,
                rule,
            ):

                activated_rules.append(rule)

        return activated_rules

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _match_rule(
        self,
        question: str,
        rule: Rule,
    ) -> bool:
        """
        Returns True if one keyword matches.
        """

        for keyword in rule.keywords:

            if keyword.lower() in question:

                return True

        return False

    # ==========================================================
    # DEBUG
    # ==========================================================

    def explain(
        self,
        question: str,
    ) -> None:
        """
        Display which rules matched.
        Useful during development.
        """

        activated = self.evaluate(question)

        print("\n" + "=" * 100)
        print("RULE ENGINE")
        print("=" * 100)

        if not activated:

            print("No rule matched.")

        else:

            for rule in activated:

                print(f"✓ {rule.name}")

        print("=" * 100)
        print()