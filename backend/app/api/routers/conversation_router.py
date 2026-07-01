from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

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
    response_model=ConversationSummary,
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

    return conversation

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