from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

import json

from sqlalchemy.orm import Session

from app.dependencies.database import (
    get_immo_db,
)

from app.dependencies.conversation import (
    get_conversation_service,
)

from app.api.models.conversation_models import (
    CreateConversationRequest,
    CreateConversationResponse,
    ConversationSummary,
    ConversationDetails,
    UpdateConversationRequest,
)

from app.services.conversation_service import (
    ConversationService,
)

router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=CreateConversationResponse,
)
def create_conversation(
    request: CreateConversationRequest,
    db: Session = Depends(get_immo_db),
):
    service = get_conversation_service(db)

    conversation = service.create(
        title=request.title,
        user_id=request.user_id,
    )

    return conversation


@router.get(
    "",
    response_model=list[ConversationSummary],
)
def get_conversations(
    db: Session = Depends(get_immo_db),
):
    service = get_conversation_service(db)

    return service.get_all()

@router.get(
    "/{conversation_uuid}",
    response_model=ConversationDetails,
)
def get_conversation(
    conversation_uuid: str,
    db: Session = Depends(get_immo_db),
):

    service = get_conversation_service(db)

    conversation = service.get_by_uuid(
        conversation_uuid
    )

    if conversation is None:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    messages = []

    for message in conversation.messages:

        rows = None

        if message.result_json:

            rows = json.loads(
                message.result_json
            )

        messages.append({

            "role": message.role,

            "content": message.content,

            "generated_sql": message.generated_sql,

            "rows": rows,

            "rows_returned": message.rows_returned,

            "execution_time_ms": message.execution_time_ms,

            "status": message.status,

            "created_at": message.created_at,

        })

    return {

        "id": conversation.id,

        "conversation_uuid": conversation.conversation_uuid,

        "title": conversation.title,

        "status": conversation.status,

        "created_at": conversation.created_at,

        "updated_at": conversation.updated_at,

        "messages": messages,

    }

@router.patch(
    "/{conversation_uuid}",
    response_model=ConversationSummary,
)
def rename_conversation(
    conversation_uuid: str,
    request: UpdateConversationRequest,
    db: Session = Depends(get_immo_db),
):

    service = get_conversation_service(db)

    conversation = service.get_by_uuid(
        conversation_uuid
    )

    if conversation is None:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return service.rename(
        conversation,
        request.title,
    )

@router.delete(
    "/{conversation_uuid}",
)
def delete_conversation(
    conversation_uuid: str,
    db: Session = Depends(get_immo_db),
):

    service = get_conversation_service(db)

    conversation = service.get_by_uuid(
        conversation_uuid
    )

    if conversation is None:

        raise HTTPException(

            status_code=404,

            detail="Conversation not found.",

        )

    service.delete(
        conversation
    )

    return {

        "success": True

    }