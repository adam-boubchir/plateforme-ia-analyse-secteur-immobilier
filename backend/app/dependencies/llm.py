from __future__ import annotations

from sqlalchemy.orm import (
    Session,
)

from app.agents.orchestrator.orchestrator_generator import (
    OrchestratorGenerator,
)
from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
)
from app.services.llm_service import (
    LLMService,
)
from app.services.model_manager import (
    ModelManager,
)

__all__ = (
    "get_model_manager",
    "get_llm_service",
    "get_sql_generator",
    "get_orchestrator_generator",
)


# ==========================================================
# MODEL MANAGER
# ==========================================================


def get_model_manager(
    *,
    db: Session,
) -> ModelManager:
    """
    Build and return the ModelManager.

    Args:
        db:
            Application database session.

    Returns:
        Configured ModelManager instance.
    """

    model_manager = ModelManager(
        db=db,
    )

    return model_manager


# ==========================================================
# LLM SERVICE
# ==========================================================


def get_llm_service(
    *,
    db: Session,
) -> LLMService:
    """
    Build and return the LLMService.

    Args:
        db:
            Application database session.

    Returns:
        Configured LLMService instance.
    """

    model_manager = get_model_manager(
        db=db,
    )

    llm_service = LLMService(
        model_manager=model_manager,
    )

    return llm_service


# ==========================================================
# SQL GENERATOR
# ==========================================================


def get_sql_generator(
    *,
    db: Session,
) -> SQLGenerator:
    """
    Build and return the SQLGenerator.

    Args:
        db:
            Application database session.

    Returns:
        Configured SQLGenerator instance.
    """

    llm_service = get_llm_service(
        db=db,
    )

    sql_generator = SQLGenerator(
        llm_service=llm_service,
    )

    return sql_generator


# ==========================================================
# ORCHESTRATOR GENERATOR
# ==========================================================


def get_orchestrator_generator(
    *,
    db: Session,
) -> OrchestratorGenerator:
    """
    Build and return the OrchestratorGenerator.

    Args:
        db:
            Application database session.

    Returns:
        Configured OrchestratorGenerator instance.
    """

    llm_service = get_llm_service(
        db=db,
    )

    orchestrator_generator = OrchestratorGenerator(
        llm_service=llm_service,
    )

    return orchestrator_generator