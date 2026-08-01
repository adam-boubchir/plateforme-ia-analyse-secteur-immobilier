from sqlalchemy.orm import Session

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

from app.agents.sql_agent.few_shots.examples import (
    FEW_SHOT_EXAMPLES,
)

from app.agents.sql_agent.context_engine.selectors.knowledge_selector import (
    KnowledgeSelector,
)

from app.agents.sql_agent.context_engine.selectors.rule_engine import (
    RuleEngine,
)

from app.agents.sql_agent.context_engine.selectors.scoring import (
    RuleScorer,
)

from app.agents.sql_agent.context_engine.selectors.rules import (
    RULES,
)

from app.agents.sql_agent.entity_detector import (
    EntityDetector,
)

from app.agents.sql_agent.few_shot_provider import (
    FewShotProvider,
)

def get_sql_agent(
    immo_db: Session,
    ministry_db: Session,
) -> SQLAgent:
    """
    Dependency responsible for building the SQL Agent.

    Pipeline
    --------
    Context Builder
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
    """

    context_builder = get_sql_context_builder(
        db=immo_db,
    )

    few_shot_provider = FewShotProvider(
        examples=FEW_SHOT_EXAMPLES,
    )

    entity_detector = EntityDetector()

    rule_engine = RuleEngine(
        rules=RULES,
    )

    rule_scorer = RuleScorer()

    selector = KnowledgeSelector(
        entity_detector=entity_detector,
        rule_engine=rule_engine,
        rule_scorer=rule_scorer,
    )

    prompt_builder = PromptBuilder(
        few_shot_provider=few_shot_provider,
    )

    generator: SQLGenerator = get_sql_generator(
        db=immo_db,
    )

    validator = SQLValidator()

    executor = SQLExecutor(
        db=ministry_db,
    )

    formatter = SQLResponseFormatter()

    log_service = get_log_service(
        db=immo_db,
    )

    execution_logger = ExecutionLogger(
        log_service=log_service,
    )

    return SQLAgent(
        selector=selector,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generator=generator,
        validator=validator,
        executor=executor,
        formatter=formatter,
        execution_logger=execution_logger,
    )

__all__ = [
    "get_sql_agent",
]