from __future__ import annotations

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import (
    Session,
)

from app.api.models.chat_models import (
    ChatRequest,
    ChatResponse,
)
from app.dependencies.chat import (
    get_chat_service,
)
from app.dependencies.database import (
    get_immo_db,
    get_ministry_db,
)
from app.services.chat_service import (
    ChatService,
)

__all__ = (
    "router",
)

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

# ==========================================================
# TYPE ALIASES
# ==========================================================

ImmoDatabase = Annotated[
    Session,
    Depends(get_immo_db),
]

MinistryDatabase = Annotated[
    Session,
    Depends(get_ministry_db),
]

ChatServiceDependency = Annotated[
    ChatService,
    Depends(get_chat_service),
]

# ==========================================================
# CHAT
# ==========================================================


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    *,
    request: ChatRequest,
    service: ChatServiceDependency,
) -> ChatResponse:
    """
    Process a user question through the AI platform.

    Workflow:
        Client
            ↓
        Chat Router
            ↓
        Chat Service
            ↓
        AI Orchestrator
            ↓
        Response

    Args:
        request:
            User request containing the question and an optional
            conversation UUID.

        service:
            Chat service injected by FastAPI.

    Returns:
        Chat response returned to the frontend.
    """

    result = service.chat(
        question=request.question,
        conversation_uuid=request.conversation_uuid,
    )

    response = ChatResponse(
        success=result.success,
        conversation_uuid=result.conversation_uuid,
        answer=result.answer,
        sql=result.sql,
        rows=result.rows,
        error=result.error,
    )

    return response