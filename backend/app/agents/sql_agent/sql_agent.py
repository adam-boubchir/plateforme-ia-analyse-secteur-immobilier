import json

from app.agents.sql_agent.context_engine.sql_context_builder import (
    SQLContextBuilder,
)

from app.agents.sql_agent.context_engine.selectors.knowledge_selector import (
    KnowledgeSelector,
)

from app.agents.sql_agent.prompts import (
    PromptBuilder,
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

from app.logging.execution_logger import (
    ExecutionLogger,
)

from app.models.sql_agent_models import (
    SQLAgentResponse,
)


class SQLAgent:
    """
    SQL Agent.

    Pipeline

    Question
        ↓
    Knowledge Selection
        ↓
    Context Building
        ↓
    Prompt Building
        ↓
    SQL Generation
        ↓
    Validation
        ↓
    Execution
        ↓
    Response Formatting
    """

    def __init__(
        self,
        context_builder: SQLContextBuilder,
        prompt_builder: PromptBuilder,
        generator: SQLGenerator,
        validator: SQLValidator,
        executor: SQLExecutor,
        formatter: SQLResponseFormatter,
        execution_logger: ExecutionLogger,
    ):

        self.selector = KnowledgeSelector()

        self.context_builder = context_builder

        self.prompt_builder = prompt_builder

        self.generator = generator

        self.validator = validator

        self.executor = executor

        self.formatter = formatter

        self.execution_logger = execution_logger

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def ask(
        self,
        question: str,
        conversation_id: int,
    ) -> SQLAgentResponse:
        """
        Execute the complete SQL Agent pipeline.
        """

        execution = self.execution_logger.start(

            question=question,

            conversation_id=conversation_id,

        )

        try:

            # --------------------------------------------------
            # KNOWLEDGE SELECTION
            # --------------------------------------------------

            selection = self.selector.select(
                question
            )

            execution.selected_tables = ", ".join(
                selection["tables"]
            )

            # --------------------------------------------------
            # CONTEXT
            # --------------------------------------------------

            context_data = self.context_builder.build_context(

                question=question,

                selection=selection,

            )

            print("=" * 100)
            print("CONTEXT DATA")
            print(context_data)
            print("=" * 100)
            for key, value in context_data.items():
                print(f"\n----- {key} -----")
                print(value)

            print("=" * 100 + "\n")

            execution.business_knowledge = context_data.get(
                "business_knowledge",
                "",
            )

            print("Execution Business")
            print(execution.business_knowledge)

            print("Execution Join")
            print(execution.join_knowledge)

            print("Execution Forbidden")
            print(execution.forbidden_joins)

            print("Execution Semantic")
            print(execution.semantic_context)

            execution.join_knowledge = context_data.get(
                "join_knowledge",
                "",
            )

            execution.forbidden_joins = context_data.get(
                "forbidden_joins",
                "",
            )

            execution.semantic_context = context_data.get(
                "semantic_context",
                "",
            )

            if hasattr(execution, "sql_patterns"):
                execution.sql_patterns = context_data.get(
                    "sql_patterns",
                    "",
                )

            execution.full_context = context_data.get(
                "full_context",
                "",
            )

            print("\n" + "=" * 100)
            print("AFTER ASSIGNMENT")
            print("=" * 100)

            print("business_knowledge :", repr(execution.business_knowledge))
            print("join_knowledge     :", repr(execution.join_knowledge))
            print("forbidden_joins    :", repr(execution.forbidden_joins))
            print("semantic_context   :", repr(execution.semantic_context))
            print("sql_patterns       :", repr(execution.sql_patterns))
            print("full_context       :", repr(execution.full_context))

            print("=" * 100 + "\n")

            # --------------------------------------------------
            # PROMPT
            # --------------------------------------------------

            prompt = self.prompt_builder.build_prompt(

                question=question,

                context=context_data["full_context"],

                selection=selection,

            )

            execution.prompt = prompt

            # --------------------------------------------------
            # SQL GENERATION
            # --------------------------------------------------

            sql = self.generator.generate(
                prompt
            )

            execution.generated_sql = sql

            if not sql:

                raise ValueError(
                    "EMPTY_SQL"
                )

            if sql == "CANNOT_GENERATE_SQL":

                execution.error = "CANNOT_GENERATE_SQL"

                print("\n" + "=" * 100)
                print("BEFORE SAVE")
                print("=" * 100)

                print("business_knowledge :", repr(execution.business_knowledge))
                print("join_knowledge     :", repr(execution.join_knowledge))
                print("forbidden_joins    :", repr(execution.forbidden_joins))
                print("semantic_context   :", repr(execution.semantic_context))
                print("sql_patterns       :", repr(execution.sql_patterns))
                print("full_context       :", repr(execution.full_context))

                print("=" * 100 + "\n")

                self.execution_logger.finish(
                    execution
                )

                return SQLAgentResponse(

                    success=False,

                    answer=(
                        "Je ne peux pas répondre à cette question "
                        "avec les données actuellement disponibles."
                    ),

                    sql=None,

                    rows=[],

                    error="CANNOT_GENERATE_SQL",

                )

            # --------------------------------------------------
            # VALIDATION
            # --------------------------------------------------

            sql = self.validator.validate(
                sql
            )

            execution.validated_sql = sql

            # --------------------------------------------------
            # EXECUTION
            # --------------------------------------------------

            rows = self.executor.execute(
                sql
            )

            execution.sql_result = json.dumps(

                rows,

                ensure_ascii=False,

                default=str,

            )

            # --------------------------------------------------
            # RESPONSE
            # --------------------------------------------------

            answer = self.formatter.format(
                rows
            )

            execution.formatted_answer = answer

            # --------------------------------------------------
            # FINISH
            # --------------------------------------------------

            self.execution_logger.finish(
                execution
            )

            return SQLAgentResponse(

                success=True,

                answer=answer,

                sql=sql,

                rows=rows,

                error=None,

            )

        except Exception as ex:

            self.execution_logger.fail(

                execution,

                ex,

            )

            raise