from __future__ import annotations

import json
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.models.conversation_models import (
    ConversationDetails,
    ConversationSummary,
    CreateConversationRequest,
    CreateConversationResponse,
    UpdateConversationRequest,
)
from app.dependencies.conversation import (
    get_conversation_service,
)
from app.dependencies.database import (
    get_immo_db,
)
from app.dependencies.log import (
    get_log_service,
)
from app.services.conversation_service import (
    ConversationService,
)
from app.services.log_service import (
    LogService,
)

__all__ = ("router",)

router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["Conversations"],
)

DbSession = Annotated[
    Session,
    Depends(get_immo_db),
]

ConversationServiceDep = Annotated[
    ConversationService,
    Depends(get_conversation_service),
]

LogServiceDep = Annotated[
    LogService,
    Depends(get_log_service),
]


# ==========================================================
# PRIVATE
# ==========================================================

def _serialize_message(
    message,
) -> dict:
    rows = None

    if message.result_json:
        rows = json.loads(
            message.result_json,
        )

    return {
        "role": message.role,
        "content": message.content,
        "generated_sql": message.generated_sql,
        "rows": rows,
        "rows_returned": message.rows_returned,
        "execution_time_ms": message.execution_time_ms,
        "status": message.status,
        "pdf_path": message.pdf_path,
        "created_at": message.created_at,
    }


# ==========================================================
# ROUTES
# ==========================================================

@router.post(
    "",
    response_model=CreateConversationResponse,
)
def create_conversation(
    request: CreateConversationRequest,
    service: ConversationServiceDep,
):
    return service.create(
        title=request.title,
        user_id=request.user_id,
    )


@router.get(
    "",
    response_model=list[ConversationSummary],
)
def get_conversations(
    service: ConversationServiceDep,
):
    return service.get_all()


@router.get(
    "/{conversation_uuid}",
    response_model=ConversationDetails,
)
def get_conversation(
    conversation_uuid: str,
    service: ConversationServiceDep,
):
    conversation = service.get_by_uuid(
        conversation_uuid=conversation_uuid,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "id": conversation.id,
        "conversation_uuid": conversation.conversation_uuid,
        "title": conversation.title,
        "status": conversation.status,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [
            _serialize_message(message)
            for message in conversation.messages
        ],
    }


@router.patch(
    "/{conversation_uuid}",
    response_model=ConversationSummary,
)
def rename_conversation(
    conversation_uuid: str,
    request: UpdateConversationRequest,
    service: ConversationServiceDep,
):
    conversation = service.get_by_uuid(
        conversation_uuid=conversation_uuid,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return service.rename(
        conversation=conversation,
        title=request.title,
    )


@router.delete(
    "/{conversation_uuid}",
)
def delete_conversation(
    conversation_uuid: str,
    service: ConversationServiceDep,
):
    conversation = service.get_by_uuid(
        conversation_uuid=conversation_uuid,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    service.delete(
        conversation=conversation,
    )

    return {
        "success": True,
    }


@router.get(
    "/{conversation_uuid}/logs",
)
def get_conversation_logs(
    conversation_uuid: str,
    service: ConversationServiceDep,
    log_service: LogServiceDep,
):
    conversation = service.get_by_uuid(
        conversation_uuid=conversation_uuid,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    logs = log_service.get_logs_by_conversation(
        conversation_id=conversation.id,
    )

    return {
        "success": True,
        "conversation_uuid": conversation_uuid,
        "conversation_title": conversation.title,
        "logs": [
            {
                "id": log.id,
                "question": log.question,
                "status": log.status,
                "execution_time_ms": log.execution_time_ms,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }