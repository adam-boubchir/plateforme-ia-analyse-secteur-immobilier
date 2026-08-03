from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.chat_agent.chat_agent import ChatAgent
from app.agents.chat_agent.chat_generator import ChatGenerator
from app.agents.chat_agent.chat_prompt_builder import ChatPromptBuilder
from app.dependencies.llm import get_llm_service


# ==========================================================
# CHAT GENERATOR
# ==========================================================

def get_chat_generator(
    db: Session,
) -> ChatGenerator:
    """
    Create and configure the ChatGenerator.
    """

    chat_generator = ChatGenerator(
        llm_service=get_llm_service(
            db=db,
        ),
    )

    return chat_generator


# ==========================================================
# CHAT AGENT
# ==========================================================

def get_chat_agent(
    db: Session,
) -> ChatAgent:
    """
    Create and configure the ChatAgent.
    """

    chat_agent = ChatAgent(
        prompt_builder=ChatPromptBuilder(),
        generator=get_chat_generator(
            db=db,
        ),
    )

    return chat_agent