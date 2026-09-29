from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

from app.agents.orchestrator.agent_registry import (
    AgentRegistry,
)

from app.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
)

from app.agents.orchestrator.orchestrator_prompt_builder import (
    OrchestratorPromptBuilder,
)

from app.agents.orchestrator.orchestrator_service import (
    OrchestratorService,
)

from app.dependencies.chat_agent import (
    get_chat_agent,
)

from app.dependencies.database import (
    get_immo_db,
    get_ministry_db,
)

from app.dependencies.llm import (
    get_orchestrator_generator,
)

from app.dependencies.prediction_agent import (
    get_prediction_agent,
)

from app.dependencies.report_agent import (
    get_report_agent,
)

from app.dependencies.sql_agent import (
    get_sql_agent,
)


__all__ = (
    "get_orchestrator_agent",
    "get_agent_registry",
    "get_orchestrator_service",
)


# ==========================================================
# TYPE ALIASES
# ==========================================================

ImmoDatabase = Annotated[
    Session,
    Depends(get_immo_db),
]

MinistryDatabase = Annotated[
    Session,
    Depends(get_ministry_db),
]


# ==========================================================
# ORCHESTRATOR AGENT
# ==========================================================

def get_orchestrator_agent(
    *,
    db: ImmoDatabase,
) -> OrchestratorAgent:
    """
    Build and return the OrchestratorAgent.
    """

    prompt_builder = OrchestratorPromptBuilder()

    generator = get_orchestrator_generator(
        db=db,
    )

    orchestrator_agent = OrchestratorAgent(
        prompt_builder=prompt_builder,
        generator=generator,
    )

    return orchestrator_agent


# ==========================================================
# AGENT REGISTRY
# ==========================================================

def get_agent_registry(
    *,
    immo_db: ImmoDatabase,
    ministry_db: MinistryDatabase,
) -> AgentRegistry:
    """
    Build and return the AgentRegistry.
    """

    # ======================================================
    # SQL AGENT
    # ======================================================

    sql_agent = get_sql_agent(
        immo_db=immo_db,
        ministry_db=ministry_db,
    )

    # ======================================================
    # CHAT AGENT
    # ======================================================

    chat_agent = get_chat_agent(
        db=immo_db,
    )

    # ======================================================
    # REPORT AGENT
    # ======================================================

    report_agent = get_report_agent(
        db=immo_db,
        sql_agent=sql_agent,
    )

    # ======================================================
    # PREDICTION AGENT
    # ======================================================

    prediction_agent = get_prediction_agent(
        sql_agent=sql_agent,
    )

    # ======================================================
    # AGENT REGISTRY
    # ======================================================

    agent_registry = AgentRegistry(
        sql_agent=sql_agent,
        chat_agent=chat_agent,
        report_agent=report_agent,
        prediction_agent=prediction_agent,
    )

    return agent_registry


# ==========================================================
# ORCHESTRATOR SERVICE
# ==========================================================

def get_orchestrator_service(
    *,
    immo_db: ImmoDatabase,
    ministry_db: MinistryDatabase,
) -> OrchestratorService:
    """
    Build and return the OrchestratorService.
    """

    orchestrator_agent = get_orchestrator_agent(
        db=immo_db,
    )

    agent_registry = get_agent_registry(
        immo_db=immo_db,
        ministry_db=ministry_db,
    )

    orchestrator_service = OrchestratorService(
        orchestrator_agent=orchestrator_agent,
        agent_registry=agent_registry,
    )

    return orchestrator_service