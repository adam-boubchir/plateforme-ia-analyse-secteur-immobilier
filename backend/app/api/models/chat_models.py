from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request sent by the frontend.
    """

    conversation_uuid: str | None = None

    question: str = Field(
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):
    """
    Response returned to the frontend.
    """

    success: bool

    conversation_uuid: str | None = None

    answer: str

    sql: str | None = None

    rows: list[dict] = []

    error: str | None = None