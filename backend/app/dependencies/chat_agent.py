from sqlalchemy.orm import Session

from app.agents.chat_agent.chat_agent import (
    ChatAgent,
)

from app.agents.chat_agent.chat_generator import (
    ChatGenerator,
)

from app.agents.chat_agent.chat_prompt_builder import (
    ChatPromptBuilder,
)

from app.dependencies.llm import (
    get_llm_service,
)


# ==========================================================
# CHAT GENERATOR
# ==========================================================

def get_chat_generator(
    db: Session,
) -> ChatGenerator:
    """
    Dependency responsible for creating the ChatGenerator.
    """

    return ChatGenerator(

        get_llm_service(
            db
        )

    )


# ==========================================================
# CHAT AGENT
# ==========================================================

def get_chat_agent(
    db: Session,
) -> ChatAgent:
    """
    Dependency responsible for creating the ChatAgent.
    """

    prompt_builder = ChatPromptBuilder()

    generator = get_chat_generator(
        db
    )

    return ChatAgent(

        prompt_builder=prompt_builder,

        generator=generator,

    )