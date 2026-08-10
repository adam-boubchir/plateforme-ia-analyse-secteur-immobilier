from __future__ import annotations

from app.agents.base.base_agent import BaseAgent
from app.agents.report_agent.report_engine import ReportEngine
from app.agents.report_agent.report_models import ReportRequest
from app.agents.sql_agent.sql_agent import SQLAgent
from app.logging.execution_logger import ExecutionLogger
from app.models.agent_response import AgentResponse
from app.models.sql_agent_models import SQLAgentResponse

__all__ = (
    "ReportAgent",
)


class ReportAgent(BaseAgent):
    """
    AI agent responsible for generating analytical reports.

    Workflow
    --------
    Question
        ↓
    SQL Agent
        ↓
    SQL Result
        ↓
    Report Engine
        ↓
    Agent Response
    """

    def __init__(
        self,
        *,
        sql_agent: SQLAgent,
        report_engine: ReportEngine,
        execution_logger: ExecutionLogger,
    ) -> None:
        self._sql_agent = sql_agent
        self._report_engine = report_engine
        self._execution_logger = execution_logger

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def ask(
        self,
        *,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:
        """
        Generate an analytical report from a natural language question.
        """

        execution = self._execution_logger.start(
            question=question,
            conversation_id=conversation_id,
        )

        try:

            sql_response = self._execute_sql(
                question=question,
                conversation_id=conversation_id,
            )

            if not sql_response.success:

                response = self._build_sql_error_response(
                    sql_response=sql_response,
                )

            else:

                response = self._generate_report(
                    question=question,
                    sql_response=sql_response,
                )

            self._execution_logger.finish(
                context=execution,
            )

            return response

        except Exception as ex:

            self._execution_logger.fail(
                context=execution,
                error=ex,
            )

            raise

    # ==========================================================
    # SQL
    # ==========================================================

    def _execute_sql(
        self,
        *,
        question: str,
        conversation_id: int,
    ) -> SQLAgentResponse:
        """
        Execute the SQL agent.
        """

        return self._sql_agent.ask(
            question=question,
            conversation_id=conversation_id,
        )

    # ==========================================================
    # REPORT
    # ==========================================================

    def _generate_report(
        self,
        *,
        question: str,
        sql_response: SQLAgentResponse,
    ) -> AgentResponse:
        """
        Generate the analytical report.
        """

        request = ReportRequest(
            question=question,
            sql=sql_response.sql or "",
            rows=sql_response.rows,
        )

        report = self._report_engine.generate(
            request=request,
        )

        return AgentResponse(
            success=True,
            answer=report.markdown,
            sql=sql_response.sql,
            rows=sql_response.rows,
            data=report,
            pdf_path=report.pdf_path,
        )

    # ==========================================================
    # RESPONSE
    # ==========================================================

    @staticmethod
    def _build_sql_error_response(
        *,
        sql_response: SQLAgentResponse,
    ) -> AgentResponse:
        """
        Build the response returned when SQL generation fails.
        """

        return AgentResponse(
            success=False,
            answer=sql_response.answer,
            sql=sql_response.sql,
            rows=sql_response.rows,
            error=sql_response.error,
        )