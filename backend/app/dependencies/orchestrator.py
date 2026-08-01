from sqlalchemy.orm import Session

from app.agents.chat_agent.chat_agent import (
    ChatAgent,
)
from app.agents.orchestrator.agent_registry import (
    AgentRegistry,
)
from app.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
)
from app.agents.orchestrator.orchestrator_generator import (
    OrchestratorGenerator,
)
from app.agents.orchestrator.orchestrator_prompt_builder import (
    OrchestratorPromptBuilder,
)
from app.agents.orchestrator.orchestrator_service import (
    OrchestratorService,
)
from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)
from app.dependencies.chat_agent import (
    get_chat_agent,
)
from app.dependencies.llm import (
    get_orchestrator_generator,
)
from app.dependencies.sql_agent import (
    get_sql_agent,
)


# ==========================================================
# ORCHESTRATOR AGENT
# ==========================================================

def get_orchestrator_agent(
    db: Session,
) -> OrchestratorAgent:
    """
    Build the OrchestratorAgent dependency.
    """

    prompt_builder = OrchestratorPromptBuilder()

    generator: OrchestratorGenerator = (
        get_orchestrator_generator(
            db=db,
        )
    )

    return OrchestratorAgent(
        prompt_builder=prompt_builder,
        generator=generator,
    )


# ==========================================================
# AGENT REGISTRY
# ==========================================================

def get_agent_registry(
    immo_db: Session,
    ministry_db: Session,
) -> AgentRegistry:
    """
    Build the AgentRegistry dependency.
    """

    sql_agent: SQLAgent = get_sql_agent(
        immo_db=immo_db,
        ministry_db=ministry_db,
    )

    chat_agent: ChatAgent = get_chat_agent(
        db=immo_db,
    )

    return AgentRegistry(
        sql_agent=sql_agent,
        chat_agent=chat_agent,
    )


# ==========================================================
# ORCHESTRATOR SERVICE
# ==========================================================

def get_orchestrator_service(
    immo_db: Session,
    ministry_db: Session,
) -> OrchestratorService:
    """
    Build the OrchestratorService dependency.
    """

    orchestrator_agent: OrchestratorAgent = (
        get_orchestrator_agent(
            db=immo_db,
        )
    )

    agent_registry: AgentRegistry = (
        get_agent_registry(
            immo_db=immo_db,
            ministry_db=ministry_db,
        )
    )

    return OrchestratorService(
        orchestrator_agent=orchestrator_agent,
        agent_registry=agent_registry,
    )


__all__ = [
    "get_orchestrator_agent",
    "get_agent_registry",
    "get_orchestrator_service",
]