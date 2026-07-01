from typing import Any

from pydantic import BaseModel


class SQLAgentResponse(BaseModel):
    """
    Response returned by the SQL Agent.
    """

    success: bool

    conversation_uuid: str | None = None

    answer: str

    sql: str | None = None

    rows: list[dict[str, Any]] = []

    error: str | None = None