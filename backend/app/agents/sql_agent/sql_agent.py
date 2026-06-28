from app.agents.sql_agent.sql_context_builder import (
    SQLContextBuilder,
)

from app.agents.sql_agent.prompts import (
    PromptBuilder,
)

from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
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

from app.models.sql_agent_models import (
    SQLAgentResponse,
)


class SQLAgent:
    """
    Main SQL Agent orchestrator.
    """

    def __init__(
        self,
        context_builder: SQLContextBuilder,
        prompt_builder: PromptBuilder,
        generator: SQLGenerator,
        validator: SQLValidator,
        executor: SQLExecutor,
        formatter: SQLResponseFormatter,
    ):

        self.context_builder = context_builder

        self.prompt_builder = prompt_builder

        self.generator = generator

        self.validator = validator

        self.executor = executor

        self.formatter = formatter

    def ask(
        self,
        question: str,
    ) -> SQLAgentResponse:

        context = self.context_builder.build_context()

        prompt = self.prompt_builder.build_prompt(
            question=question,
            context=context,
        )

        sql = self.generator.generate(
            prompt
        ).strip()

        sql = self.validator.validate(
            sql
        )

        rows = self.executor.execute(
            sql
        )

        answer = self.formatter.format(
            rows
        )

        return SQLAgentResponse(

            success=True,

            answer=answer,

            sql=sql,

            rows=rows,

            error=None,
        )