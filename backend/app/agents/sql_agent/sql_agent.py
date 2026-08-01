from __future__ import annotations

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

from app.agents.base.base_agent import (
    BaseAgent,
)

from typing import Any

from app.database.entities.conversation_log import ConversationLog

from app.agents.sql_agent.exceptions import (
    CannotGenerateSQLException,
    EmptySQLQueryException,
)

__all__ = ["SQLAgent"]

CANNOT_GENERATE_SQL_ERROR = "CANNOT_GENERATE_SQL"
EMPTY_SQL_ERROR = "EMPTY_SQL"

class SQLAgent(BaseAgent):
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
        selector: KnowledgeSelector,
        context_builder: SQLContextBuilder,
        prompt_builder: PromptBuilder,
        generator: SQLGenerator,
        validator: SQLValidator,
        executor: SQLExecutor,
        formatter: SQLResponseFormatter,
        execution_logger: ExecutionLogger,
    ) -> None:
        self.selector = selector
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.validator = validator
        self.executor = executor
        self.formatter = formatter
        self.execution_logger = execution_logger


    def _select_knowledge(
        self,
        question: str,
        execution: ConversationLog,
    ) -> dict[str, Any]:

        selection = self.selector.select(
            question
        )

        execution.selected_tables = ", ".join(
            selection["tables"]
        )

        return selection

    def _build_context(
        self,
        question: str,
        selection: dict[str, Any],
        execution: ConversationLog,
    ) -> dict[str, Any]:

        context_data = self.context_builder.build_context(
            question=question,
            selection=selection,
        )

        self._populate_execution_context(
            execution,
            context_data,
        )

        return context_data

    def _build_prompt(
        self,
        question,
        context_data,
        selection,
        execution,
    ) -> str:

        prompt = self.prompt_builder.build_prompt(
            question=question,
            context=context_data.get(
                "full_context",
                "",
            ),
            selection=selection,
        )

        execution.prompt = prompt

        return prompt

    def _generate_sql(
        self,
        prompt,
        execution,
    ) -> str:

        sql = self.generator.generate(prompt)

        execution.generated_sql = sql

        if not sql:
            raise EmptySQLQueryException()

        if sql == CANNOT_GENERATE_SQL_ERROR:
            raise CannotGenerateSQLException()

        sql = self.validator.validate(sql)

        execution.validated_sql = sql

        return sql

    def _execute_sql(
        self,
        sql,
        execution,
    ) -> list[dict[str, Any]]:

        rows = self.executor.execute(sql)

        execution.sql_result = json.dumps(
            rows,
            ensure_ascii=False,
            default=str,
        )

        return rows

    def _format_response(
        self,
        rows,
        execution,
    ) -> str:

        answer = self.formatter.format(rows)

        execution.formatted_answer = answer

        return answer

    def _populate_execution_context(
        self,
        execution: ConversationLog,
        context_data: dict[str, Any],
    ) -> None:
        """
        Populate the execution log with the generated context.
        """

        execution.business_knowledge = context_data.get(
            "business_knowledge",
            "",
        )

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

        execution.sql_patterns = context_data.get(
            "sql_patterns",
            "",
        )

        execution.full_context = context_data.get(
            "full_context",
            "",
        )

    def _execute_pipeline(
        self,
        question: str,
        execution: ConversationLog,
    ) -> SQLAgentResponse:
        """
        Execute the complete SQL processing pipeline for a user question.
        """

        selection = self._select_knowledge(
            question,
            execution,
        )

        context_data = self._build_context(
            question,
            selection,
            execution,
        )

        prompt = self._build_prompt(
            question,
            context_data,
            selection,
            execution,
        )

        sql = self._generate_sql(
            prompt,
            execution,
        )

        rows = self._execute_sql(
            sql,
            execution,
        )

        answer = self._format_response(
            rows,
            execution,
        )

        return self._success_response(
            answer=answer,
            sql=sql,
            rows=rows,
        )

    def _cannot_generate_response(self) -> SQLAgentResponse:
        """
        Build the response returned when no SQL query can be generated.
        """

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

    def _success_response(
        self,
        answer: str,
        sql: str,
        rows: list[dict],
    ) -> SQLAgentResponse:
        """
        Build the response returned after a successful SQL execution.
        """

        return SQLAgentResponse(
            success=True,
            answer=answer,
            sql=sql,
            rows=rows,
            error=None,
        )

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

            response = self._execute_pipeline(
                question,
                execution,
            )

            self.execution_logger.finish(
                execution,
            )

            return response

        except CannotGenerateSQLException:

            execution.error = CANNOT_GENERATE_SQL_ERROR

            self.execution_logger.finish(
                execution,
            )

            return self._cannot_generate_response()

        except EmptySQLQueryException as ex:

            self.execution_logger.fail(
                execution,
                ex,
            )

            raise

        except Exception as ex:

            self.execution_logger.fail(
                execution,
                ex,
            )

            raise