from sqlalchemy.orm import Session

from app.dependencies.metadata import (
    get_sql_context_builder,
)

from app.dependencies.llm import (
    get_sql_generator,
)

from app.agents.sql_agent.prompts import (
    PromptBuilder,
)

from app.agents.sql_agent.sql_validator import (
    SQLValidator,
)

from app.agents.sql_agent.sql_executor import (
    SQLExecutor,
)

from app.agents.sql_agent.sql_response_formatter import (
    SQLResponseFormatter,
)

from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)


def get_sql_agent(
    immo_db: Session,
    ministry_db: Session,
) -> SQLAgent:
    """
    Build and return the SQLAgent.
    """

    context_builder = get_sql_context_builder(
        immo_db
    )

    prompt_builder = PromptBuilder()

    generator = get_sql_generator(
        immo_db
    )

    validator = SQLValidator()

    executor = SQLExecutor(
        ministry_db
    )

    formatter = SQLResponseFormatter()

    return SQLAgent(
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        generator=generator,
        validator=validator,
        executor=executor,
        formatter=formatter,
    )