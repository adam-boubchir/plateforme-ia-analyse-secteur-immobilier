from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

__all__ = (
    "ChatRequest",
    "ChatResponse",
)


class ChatRequest(BaseModel):
    """
    Request model sent by the frontend to the chat endpoint.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    conversation_uuid: str | None = None

    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Natural language question asked by the user.",
    )


class ChatResponse(BaseModel):
    """
    Response model returned by the chat endpoint.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    success: bool

    conversation_uuid: str | None = None

    answer: str

    sql: str | None = None

    rows: list[dict[str, Any]] = Field(
        default_factory=list,
        description="SQL query result rows.",
    )

    error: str | None = None