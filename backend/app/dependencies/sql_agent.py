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
        immo_db
    )

    prompt_builder = PromptBuilder()

    generator: SQLGenerator = get_sql_generator(
        immo_db
    )

    validator = SQLValidator()

    executor = SQLExecutor(
        ministry_db
    )

    formatter = SQLResponseFormatter()

    execution_logger = ExecutionLogger(
        get_log_service(
            immo_db
        )
    )

    return SQLAgent(

        context_builder=context_builder,

        prompt_builder=prompt_builder,

        generator=generator,

        validator=validator,

        executor=executor,

        formatter=formatter,

        execution_logger=execution_logger,

    )