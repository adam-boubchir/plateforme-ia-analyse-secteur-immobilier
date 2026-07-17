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


router = APIRouter(

    prefix="/api/v1/chat",

    tags=["Chat"],

)


# ==========================================================
# CHAT
# ==========================================================

@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    immo_db: Session = Depends(
        get_immo_db
    ),
    ministry_db: Session = Depends(
        get_ministry_db
    ),
) -> ChatResponse:
    """
    Main endpoint of the AI platform.

    Workflow
    --------
    Client
        ↓
    Chat Router
        ↓
    Chat Service
        ↓
    SQL Agent
        ↓
    SQL Server
        ↓
    Chat Response
    """

    service: ChatService = get_chat_service(

        immo_db,

        ministry_db,

    )

    result = service.chat(

        question=request.question,

        conversation_uuid=request.conversation_uuid,

    )

    return ChatResponse(

        success=result.success,

        conversation_uuid=result.conversation_uuid,

        answer=result.answer,

        sql=result.sql,

        rows=result.rows,

        error=result.error,

    )