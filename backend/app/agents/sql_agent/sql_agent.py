from app.agents.sql_agent.context_engine.sql_context_builder import (
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
        """
        Execute the complete SQL Agent pipeline.
        """

        # ------------------------------------------------------------------
        # Build Context
        # ------------------------------------------------------------------

        context = self.context_builder.build_context(
            question
        )

        # ------------------------------------------------------------------
        # Build Prompt
        # ------------------------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            question=question,
            context=context,
        )

        # ------------------------------------------------------------------
        # Generate SQL
        # ------------------------------------------------------------------

        sql = self.generator.generate(
            prompt
        ).strip()

        print("\n" + "=" * 100)
        print("GENERATED SQL")
        print("=" * 100)
        print(sql)
        print("=" * 100 + "\n")

        # ------------------------------------------------------------------
        # Empty response
        # ------------------------------------------------------------------

        if not sql:

            return SQLAgentResponse(

                success=False,

                answer=(
                    "Le modèle n'a pas réussi à générer une requête SQL."
                ),

                sql=None,

                rows=[],

                error="EMPTY_SQL",

            )

        # ------------------------------------------------------------------
        # Database cannot answer
        # ------------------------------------------------------------------

        if sql == "CANNOT_GENERATE_SQL":

            return SQLAgentResponse(

                success=False,

                answer=(
                    "Je ne peux pas répondre à cette question avec les données actuellement disponibles dans la base."
                ),

                sql=None,

                rows=[],

                error="CANNOT_GENERATE_SQL",

            )

        # ------------------------------------------------------------------
        # Validate SQL
        # ------------------------------------------------------------------

        sql = self.validator.validate(
            sql
        )

        # ------------------------------------------------------------------
        # Execute SQL
        # ------------------------------------------------------------------

        rows = self.executor.execute(
            sql
        )

        # ------------------------------------------------------------------
        # Format Answer
        # ------------------------------------------------------------------

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