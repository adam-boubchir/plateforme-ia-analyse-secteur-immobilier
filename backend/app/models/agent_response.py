from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

__all__ = ("AgentResponse",)


class AgentResponse(BaseModel):
    """
    Standard response returned by every AI agent.

    This model defines the common response contract shared
    across the AI platform, regardless of the underlying agent.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

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
        default_factory=list,
    )

    # ==========================================================
    # GENERIC PAYLOAD
    # ==========================================================

    data: Any | None = None

    # ==========================================================
    # REPORT
    # ==========================================================

    pdf_path: str | None = None