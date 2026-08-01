from sqlalchemy.orm import Session

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


# ==========================================================
# MODEL MANAGER
# ==========================================================

def get_model_manager(
    db: Session,
) -> ModelManager:
    """
    Dependency responsible for creating the ModelManager.
    """

    return ModelManager(
        db=db,
    )


# ==========================================================
# LLM SERVICE
# ==========================================================

def get_llm_service(
    db: Session,
) -> LLMService:
    """
    Dependency responsible for creating the LLMService.
    """

    model_manager: ModelManager = (
        get_model_manager(
            db=db,
        )
    )

    return LLMService(
        model_manager=model_manager,
    )


# ==========================================================
# SQL GENERATOR
# ==========================================================

def get_sql_generator(
    db: Session,
) -> SQLGenerator:
    """
    Dependency responsible for creating the SQLGenerator.
    """

    llm_service: LLMService = (
        get_llm_service(
            db=db,
        )
    )

    return SQLGenerator(
        llm_service=llm_service,
    )


# ==========================================================
# ORCHESTRATOR GENERATOR
# ==========================================================

def get_orchestrator_generator(
    db: Session,
) -> OrchestratorGenerator:
    """
    Dependency responsible for creating the OrchestratorGenerator.
    """

    llm_service: LLMService = (
        get_llm_service(
            db=db,
        )
    )

    return OrchestratorGenerator(
        llm_service=llm_service,
    )


__all__ = [
    "get_model_manager",
    "get_llm_service",
    "get_sql_generator",
    "get_orchestrator_generator",
]