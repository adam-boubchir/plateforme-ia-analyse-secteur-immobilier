from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.report_agent.report_agent import (
    ReportAgent,
)
from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)
from app.dependencies.execution_logger import (
    get_execution_logger,
)
from app.dependencies.report_engine import (
    get_report_engine,
)

__all__ = (
    "get_report_agent",
)


def get_report_agent(
    *,
    db: Session,
    sql_agent: SQLAgent,
) -> ReportAgent:
    """
    Build and configure a ReportAgent.

    Dependencies
    ------------
    - SQLAgent
    - ReportEngine
    - ExecutionLogger

    Parameters
    ----------
    db:
        Application database session.

    sql_agent:
        Shared SQLAgent instance.

    Returns
    -------
    ReportAgent
        Fully configured ReportAgent instance.
    """

    report_engine = get_report_engine(
        db=db,
    )

    execution_logger = get_execution_logger(
        db=db,
    )

    return ReportAgent(
        sql_agent=sql_agent,
        report_engine=report_engine,
        execution_logger=execution_logger,
    )