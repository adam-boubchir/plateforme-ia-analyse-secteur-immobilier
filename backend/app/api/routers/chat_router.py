from fastapi import (
    APIRouter,
    Depends,
)

from app.api.models.chat_models import (
    ChatRequest,
    ChatResponse,
)

from app.dependencies.database import (
    get_immo_db,
    get_ministry_db,
)

from app.dependencies.chat import (
    get_chat_service,
)

from app.services.chat_service import (
    ChatService,
)

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    immo_db: Session = Depends(get_immo_db),
    ministry_db: Session = Depends(get_ministry_db),
) -> ChatResponse:
    """
    Main chat endpoint.
    """

    chat_service = get_chat_service(
        immo_db,
        ministry_db,
    )

    response = chat_service.chat(

        question=request.question,

        conversation_uuid=request.conversation_uuid,

    )

    return ChatResponse(

        success=response.success,

        conversation_uuid=response.conversation_uuid,

        answer=response.answer,

        sql=response.sql,

        rows=response.rows,

        error=response.error,

    )