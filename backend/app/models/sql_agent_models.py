from pydantic import BaseModel
from typing import Any


class SQLAgentResponse(BaseModel):
    """
    Response returned by the SQL Agent.
    """

    success: bool

    answer: str

    sql: str | None = None

    rows: list[dict[str, Any]] = []

    error: str | None = None