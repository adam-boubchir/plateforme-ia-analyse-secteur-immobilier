from __future__ import annotations

from typing import Any

from app.agents.sql_agent.context_engine.selectors.rule_engine import (
    RuleEngine,
)
from app.agents.sql_agent.context_engine.selectors.scoring import (
    RuleScorer,
)
from app.agents.sql_agent.entity_detector import (
    EntityDetector,
)
from app.knowledge.database_knowledge import (
    DATABASE_KNOWLEDGE,
)

__all__ = ["KnowledgeSelector"]

MIN_YEAR = 1990
MAX_YEAR = 2035

DEFAULT_SELECTION: dict[str, Any] = {
    "tables": set(),
    "business_domains": set(),
    "question_types": set(),
    "sql_patterns": set(),
    "needs_join": False,
    "aggregation": False,
    "geographic": False,
    "time_series": False,
}


class KnowledgeSelector:
    """
    Select the business knowledge required to answer a user question.

    Responsibilities
    ----------------
    - Detect entities.
    - Evaluate business rules.
    - Score activated rules.
    - Enrich the selection.
    - Produce the knowledge context.
    """

    def __init__(
        self,
        entity_detector: EntityDetector,
        rule_engine: RuleEngine,
        rule_scorer: RuleScorer,
    ) -> None:
        self.entity_detector = entity_detector
        self.rule_engine = rule_engine
        self.rule_scorer = rule_scorer

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        question: str,
    ) -> dict[str, Any]:

        entities = self._detect_entities(
            question,
        )

        scored_rules = self._score_rules(
            question,
        )

        selection = self._create_selection()

        self._apply_rules(
            selection,
            scored_rules,
        )

        self._apply_entity_enrichment(
            selection,
            entities,
        )

        self._apply_time_enrichment(
            selection,
            question,
        )

        self._apply_default_tables(
            selection,
        )

        return self._build_result(
            selection,
            entities,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_selection(
        self,
    ) -> dict[str, Any]:

        return {
            key: value.copy() if isinstance(value, set) else value
            for key, value in DEFAULT_SELECTION.items()
        }

    def _detect_entities(
        self,
        question: str,
    ) -> dict[str, Any]:

        return self.entity_detector.detect(
            question,
        )

    def _score_rules(
        self,
        question: str,
    ) -> list[tuple[Any, float]]:

        activated_rules = self.rule_engine.evaluate(
            question,
        )

        return self.rule_scorer.score(
            question,
            activated_rules,
        )

    def _apply_rules(
        self,
        selection: dict[str, Any],
        scored_rules: list[tuple[Any, float]],
    ) -> None:

        for rule, _ in scored_rules:

            selection["tables"].update(rule.tables)

            if rule.business_domain:
                selection["business_domains"].add(
                    rule.business_domain,
                )

            if rule.question_type:
                selection["question_types"].add(
                    rule.question_type,
                )

            if rule.sql_pattern:
                selection["sql_patterns"].add(
                    rule.sql_pattern,
                )

            selection["needs_join"] |= rule.needs_join
            selection["aggregation"] |= rule.aggregation
            selection["geographic"] |= rule.geographic
            selection["time_series"] |= rule.time_series

    def _apply_entity_enrichment(
        self,
        selection: dict[str, Any],
        entities: dict[str, Any],
    ) -> None:

        if entities.get("regions"):

            selection["tables"].update(
                {
                    "REGION",
                    "PROVINCE_PREFECTURE",
                }
            )

            selection["geographic"] = True

    def _apply_time_enrichment(
        self,
        selection: dict[str, Any],
        question: str,
    ) -> None:

        if any(
            str(year) in question
            for year in range(
                MIN_YEAR,
                MAX_YEAR + 1,
            )
        ):
            selection["time_series"] = True

    def _apply_default_tables(
        self,
        selection: dict[str, Any],
    ) -> None:

        if not selection["tables"]:

            selection["tables"] = set(
                DATABASE_KNOWLEDGE.keys(),
            )

    def _build_result(
        self,
        selection: dict[str, Any],
        entities: dict[str, Any],
    ) -> dict[str, Any]:

        return {
            "entities": entities,
            "tables": sorted(selection["tables"]),
            "business_domains": sorted(selection["business_domains"]),
            "question_types": sorted(selection["question_types"]),
            "sql_patterns": sorted(selection["sql_patterns"]),
            "needs_join": selection["needs_join"],
            "aggregation": selection["aggregation"],
            "geographic": selection["geographic"],
            "time_series": selection["time_series"],
        }