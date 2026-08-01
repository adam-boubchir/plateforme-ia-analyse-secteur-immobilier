from typing import Any

from pydantic import BaseModel
from pydantic import Field


class AgentResponse(BaseModel):
    """
    Standard response returned by every AI agent.
    """

    # ==========================================================
    # STATUS
    # ==========================================================

    success: bool = True

    error: str | None = None

    # ==========================================================
    # CONVERSATION
    # ==========================================================

    conversation_uuid: str | None = None

    # ==========================================================
    # MAIN RESPONSE
    # ==========================================================

    answer: str

    # ==========================================================
    # SQL AGENT
    # ==========================================================

    sql: str | None = None

    rows: list[dict[str, Any]] = Field(
        default_factory=list
    )

    # ==========================================================
    # FUTURE AGENTS
    # ==========================================================

    data: Any | None = None