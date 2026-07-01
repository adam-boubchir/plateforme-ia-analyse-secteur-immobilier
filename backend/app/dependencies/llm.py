from sqlalchemy.orm import Session

from app.services.model_manager import (
    ModelManager,
)

from app.services.llm_service import (
    LLMService,
)

from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
)


def get_model_manager(
    db: Session,
) -> ModelManager:
    """
    Dependency returning the ModelManager.
    """

    return ModelManager(db)


def get_llm_service(
    db: Session,
) -> LLMService:
    """
    Dependency returning the LLMService.
    """

    return LLMService(db)


def get_sql_generator(
    db: Session,
) -> SQLGenerator:
    """
    Dependency returning the SQLGenerator.
    """

    llm_service = get_llm_service(db)

    return SQLGenerator(llm_service)