from app.agents.sql_agent.entity_detector import (
    EntityDetector,
)

from app.knowledge.database_knowledge import (
    DATABASE_KNOWLEDGE,
)

from app.agents.sql_agent.context_engine.selectors.rule_engine import (
    RuleEngine,
)

from app.agents.sql_agent.context_engine.selectors.scoring import (
    RuleScorer,
)


class KnowledgeSelector:
    """
    Intelligent selector responsible for identifying
    the business context of the user's question.

    This class orchestrates:

        • Entity Detection
        • Rule Engine
        • Rule Scoring

    and produces the context used by the SQL Agent.
    """

    def __init__(
        self,
    ):

        self.entity_detector = EntityDetector()

        self.rule_engine = RuleEngine()

        self.rule_scorer = RuleScorer()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        question: str,
    ) -> dict:

        entities = self.entity_detector.detect(
            question
        )

        activated_rules = self.rule_engine.evaluate(
            question
        )

        scored_rules = self.rule_scorer.score(
            question,
            activated_rules,
        )

        selected_tables = set()

        business_domains = set()

        question_types = set()

        sql_patterns = set()

        needs_join = False

        aggregation = False

        geographic = False

        time_series = False

        # ======================================================
        # APPLY RULES
        # ======================================================

        for rule, score in scored_rules:

            selected_tables.update(
                rule.tables
            )

            if rule.business_domain:

                business_domains.add(
                    rule.business_domain
                )

            if rule.question_type:

                question_types.add(
                    rule.question_type
                )

            if rule.sql_pattern:

                sql_patterns.add(
                    rule.sql_pattern
                )

            needs_join |= rule.needs_join

            aggregation |= rule.aggregation

            geographic |= rule.geographic

            time_series |= rule.time_series

        # ======================================================
        # ENTITY-BASED ENRICHMENT
        # ======================================================

        if entities["regions"]:

            selected_tables.update(

                [
                    "REGION",
                    "PROVINCE_PREFECTURE",
                ]

            )

            geographic = True

        # ======================================================
        # YEAR DETECTION
        # ======================================================

        if any(

            str(year) in question

            for year in range(1990, 2036)

        ):

            time_series = True

        # ======================================================
        # DEFAULT
        # ======================================================

        if not selected_tables:

            selected_tables = set(

                DATABASE_KNOWLEDGE.keys()

            )

        # ======================================================
        # DEBUG
        # ======================================================

        self._print_debug(

            question,

            entities,

            scored_rules,

            selected_tables,

        )

        # ======================================================
        # RESULT
        # ======================================================

        return {

            "entities": entities,

            "tables": sorted(
                selected_tables
            ),

            "business_domains": sorted(
                business_domains
            ),

            "question_types": sorted(
                question_types
            ),

            "sql_patterns": sorted(
                sql_patterns
            ),

            "needs_join": needs_join,

            "aggregation": aggregation,

            "geographic": geographic,

            "time_series": time_series,

        }

    # ==========================================================
    # DEBUG
    # ==========================================================

    def _print_debug(

        self,

        question,

        entities,

        scored_rules,

        tables,

    ):

        print("\n")

        print("=" * 100)

        print("KNOWLEDGE SELECTOR")

        print("=" * 100)

        print(f"Question : {question}")

        print()

        print("Detected Entities")

        print(entities)

        print()

        print("Activated Rules")

        for rule, score in scored_rules:

            print(

                f"{score:>3}  ->  {rule.name}"

            )

        print()

        print("Selected Tables")

        for table in sorted(tables):

            print(

                f" - {table}"

            )

        print("=" * 100)

        print()