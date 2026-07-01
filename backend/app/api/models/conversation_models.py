from datetime import datetime

from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    """
    Request used to create a conversation.
    """

    title: str | None = None

    user_id: str | None = None


class ConversationSummary(BaseModel):
    """
    Conversation displayed in the sidebar.
    """

    id: int

    conversation_uuid: str

    title: str | None

    status: str

    updated_at: datetime

    class Config:

        from_attributes = True


class ConversationMessageResponse(BaseModel):
    """
    One message of a conversation.
    """

    role: str

    content: str

    generated_sql: str | None

    rows_returned: int | None

    execution_time_ms: int | None

    status: str

    created_at: datetime

    class Config:

        from_attributes = True


class ConversationDetails(BaseModel):
    """
    Complete conversation.
    """

    id: int

    conversation_uuid: str

    title: str | None

    status: str

    created_at: datetime

    updated_at: datetime

    messages: list[ConversationMessageResponse]

    class Config:

        from_attributes = True


class CreateConversationResponse(BaseModel):
    """
    Response returned after creating a conversation.
    """

    id: int

    conversation_uuid: str

    title: str | None

    status: str

    class Config:

        from_attributes = True


class DeleteConversationResponse(BaseModel):
    """
    Response returned after deleting a conversation.
    """

    success: bool