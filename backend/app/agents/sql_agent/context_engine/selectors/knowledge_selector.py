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

__all__ = ("KnowledgeSelector",)

# ==========================================================
# CONSTANTS
# ==========================================================

_MIN_YEAR = 1990
_MAX_YEAR = 2035

_DEFAULT_SELECTION: dict[str, Any] = {
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
    Select the knowledge required to answer a user question.

    Responsibilities
    ----------------
    - Detect entities.
    - Evaluate business rules.
    - Score activated rules.
    - Enrich the selection.
    - Produce the final knowledge selection.
    """

    def __init__(
        self,
        *,
        entity_detector: EntityDetector,
        rule_engine: RuleEngine,
        rule_scorer: RuleScorer,
    ) -> None:
        self._entity_detector = entity_detector
        self._rule_engine = rule_engine
        self._rule_scorer = rule_scorer

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        *,
        question: str,
    ) -> dict[str, Any]:
        """
        Build the knowledge selection for a user question.
        """

        entities = self._detect_entities(
            question=question,
        )

        scored_rules = self._score_rules(
            question=question,
        )

        selection = self._create_selection()

        self._apply_rules(
            selection=selection,
            scored_rules=scored_rules,
        )

        self._apply_entity_enrichment(
            selection=selection,
            entities=entities,
        )

        self._apply_time_enrichment(
            selection=selection,
            question=question,
        )

        self._apply_default_tables(
            selection=selection,
        )

        result = self._build_result(
            selection=selection,
            entities=entities,
        )

        return result

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _create_selection() -> dict[str, Any]:
        """
        Create a mutable selection from the default template.
        """

        selection = {
            key: value.copy() if isinstance(value, set) else value
            for key, value in _DEFAULT_SELECTION.items()
        }

        return selection

    def _detect_entities(
        self,
        *,
        question: str,
    ) -> dict[str, Any]:
        """
        Detect entities contained in the user question.
        """

        entities = self._entity_detector.detect(
            question=question,
        )

        return entities

    def _score_rules(
        self,
        *,
        question: str,
    ) -> list[tuple[Any, int]]:
        """
        Evaluate and score matching business rules.
        """

        activated_rules = self._rule_engine.evaluate(
            question=question,
        )

        scored_rules = self._rule_scorer.score(
            question=question,
            rules=activated_rules,
        )

        return scored_rules

    @staticmethod
    def _apply_rules(
        *,
        selection: dict[str, Any],
        scored_rules: list[tuple[Any, int]],
    ) -> None:
        """
        Apply activated rules to the current selection.
        """

        for rule, _ in scored_rules:

            selection["tables"].update(
                rule.tables,
            )

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

    @staticmethod
    def _apply_entity_enrichment(
        *,
        selection: dict[str, Any],
        entities: dict[str, Any],
    ) -> None:
        """
        Enrich the selection using detected entities.
        """

        if entities.get(
            "regions",
        ):

            selection["tables"].update(
                {
                    "REGION",
                    "PROVINCE_PREFECTURE",
                }
            )

            selection["geographic"] = True

    @staticmethod
    def _apply_time_enrichment(
        *,
        selection: dict[str, Any],
        question: str,
    ) -> None:
        """
        Detect explicit years in the question.
        """

        if any(
            str(year) in question
            for year in range(
                _MIN_YEAR,
                _MAX_YEAR + 1,
            )
        ):
            selection["time_series"] = True

    @staticmethod
    def _apply_default_tables(
        *,
        selection: dict[str, Any],
    ) -> None:
        """
        Select every table if no rule matched.
        """

        if not selection["tables"]:

            selection["tables"] = set(
                DATABASE_KNOWLEDGE.keys(),
            )

    @staticmethod
    def _build_result(
        *,
        selection: dict[str, Any],
        entities: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build the final immutable selection payload.
        """

        result = {
            "entities": entities,
            "tables": sorted(
                selection["tables"],
            ),
            "business_domains": sorted(
                selection["business_domains"],
            ),
            "question_types": sorted(
                selection["question_types"],
            ),
            "sql_patterns": sorted(
                selection["sql_patterns"],
            ),
            "needs_join": selection["needs_join"],
            "aggregation": selection["aggregation"],
            "geographic": selection["geographic"],
            "time_series": selection["time_series"],
        }

        return result