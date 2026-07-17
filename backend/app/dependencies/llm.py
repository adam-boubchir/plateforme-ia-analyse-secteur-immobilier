from sqlalchemy.orm import Session

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
        db
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

    return LLMService(
        db
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

    return SQLGenerator(

        get_llm_service(
            db
        )

    )