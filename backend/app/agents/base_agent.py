from abc import ABC, abstractmethod
from time import perf_counter

from sqlalchemy.orm import Session

from app.services.llm_service import LLMService


class BaseAgent(ABC):

    def __init__(
        self,
        db: Session,
        agent_name: str
    ):

        self.db = db

        self.agent_name = agent_name

        self.llm = LLMService(db)

    def execute(
        self,
        *args,
        **kwargs
    ):

        start_time = perf_counter()

        try:

            result = self._execute(
                *args,
                **kwargs
            )

            execution_time_ms = (
                perf_counter() - start_time
            ) * 1000

            return AgentExecutionResult(
                success=True,
                result=result,
                execution_time_ms=round(
                    execution_time_ms,
                    2
                )
            )

        except Exception as e:

            execution_time_ms = (
                perf_counter() - start_time
            ) * 1000

            return AgentExecutionResult(
                success=False,
                error=str(e),
                execution_time_ms=round(
                    execution_time_ms,
                    2
                )
            )

    @abstractmethod
    def _execute(
        self,
        *args,
        **kwargs
    ):
        pass