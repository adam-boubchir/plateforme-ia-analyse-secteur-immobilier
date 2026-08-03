from __future__ import annotations

from sqlalchemy.orm import (
    Session,
)

from app.agents.sql_agent.context_engine.selectors.knowledge_selector import (
    KnowledgeSelector,
)
from app.agents.sql_agent.context_engine.selectors.rule_engine import (
    RuleEngine,
)
from app.agents.sql_agent.context_engine.selectors.rules import (
    RULES,
)
from app.agents.sql_agent.context_engine.selectors.scoring import (
    RuleScorer,
)
from app.agents.sql_agent.entity_detector import (
    EntityDetector,
)
from app.agents.sql_agent.few_shot_provider import (
    FewShotProvider,
)
from app.agents.sql_agent.few_shots.examples import (
    FEW_SHOT_EXAMPLES,
)
from app.agents.sql_agent.prompts import (
    PromptBuilder,
)
from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)
from app.agents.sql_agent.sql_executor import (
    SQLExecutor,
)
from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
)
from app.agents.sql_agent.sql_response_formatter import (
    SQLResponseFormatter,
)
from app.agents.sql_agent.sql_validator import (
    SQLValidator,
)
from app.dependencies.llm import (
    get_sql_generator,
)
from app.dependencies.log import (
    get_log_service,
)
from app.dependencies.metadata import (
    get_sql_context_builder,
)
from app.logging.execution_logger import (
    ExecutionLogger,
)

__all__ = (
    "get_sql_agent",
)


# ==========================================================
# SQL AGENT
# ==========================================================


def get_sql_agent(
    *,
    immo_db: Session,
    ministry_db: Session,
) -> SQLAgent:
    """
    Build and return a fully configured SQLAgent.

    Pipeline:
        Context Builder
            ↓
        Knowledge Selector
            ↓
        Few-Shot Provider
            ↓
        Prompt Builder
            ↓
        SQL Generator
            ↓
        SQL Validator
            ↓
        SQL Executor
            ↓
        Response Formatter
            ↓
        Execution Logger

    Args:
        immo_db:
            Application database session.

        ministry_db:
            Ministry SQL Server session.

    Returns:
        Fully configured SQLAgent instance.
    """

    # ==========================================================
    # CONTEXT
    # ==========================================================

    context_builder = get_sql_context_builder(
        db=immo_db,
    )

    # ==========================================================
    # FEW SHOTS
    # ==========================================================

    few_shot_provider = FewShotProvider(
        examples=FEW_SHOT_EXAMPLES,
    )

    # ==========================================================
    # KNOWLEDGE SELECTION
    # ==========================================================

    entity_detector = EntityDetector()

    rule_engine = RuleEngine(
        rules=RULES,
    )

    rule_scorer = RuleScorer()

    knowledge_selector = KnowledgeSelector(
        entity_detector=entity_detector,
        rule_engine=rule_engine,
        rule_scorer=rule_scorer,
    )

    # ==========================================================
    # PROMPT
    # ==========================================================

    prompt_builder = PromptBuilder(
        few_shot_provider=few_shot_provider,
    )

    # ==========================================================
    # GENERATION
    # ==========================================================

    generator: SQLGenerator = get_sql_generator(
        db=immo_db,
    )

    validator = SQLValidator()

    # ==========================================================
    # EXECUTION
    # ==========================================================

    executor = SQLExecutor(
        db=ministry_db,
    )

    formatter = SQLResponseFormatter()

    # ==========================================================
    # LOGGING
    # ==========================================================

    log_service = get_log_service(
        db=immo_db,
    )

    execution_logger = ExecutionLogger(
        log_service=log_service,
    )

    # ==========================================================
    # SQL AGENT
    # ==========================================================

    sql_agent = SQLAgent(
        selector=knowledge_selector,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generator=generator,
        validator=validator,
        executor=executor,
        formatter=formatter,
        execution_logger=execution_logger,
    )

    return sql_agent