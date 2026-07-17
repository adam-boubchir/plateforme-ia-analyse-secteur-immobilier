from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.dependencies.database import (
    get_immo_db,
)

from app.dependencies.log import (
    get_log_service,
)

from app.services.log_service import (
    LogService,
)

from app.api.models.log_models import (
    LogDetailsResponse,
    LogResponse,
    LogsResponse,
    LogSummaryResponse,
)


router = APIRouter(
    prefix="/api/v1/logs",
    tags=["Logs"],
)


# ==========================================================
# GET ALL LOGS
# ==========================================================

@router.get(
    "",
    response_model=LogsResponse,
)
def get_logs(
    db: Session = Depends(get_immo_db),
) -> LogsResponse:
    """
    Return every execution log.
    """

    service: LogService = get_log_service(
        db
    )

    logs = service.get_all_logs()

    response = [

        LogSummaryResponse(

            id=log.id,

            conversation_id=log.conversation_id,

            question=log.question,

            status=log.status,

            execution_time_ms=log.execution_time_ms,

            created_at=log.created_at,

        )

        for log in logs

    ]

    return LogsResponse(

        success=True,

        logs=response,

    )


# ==========================================================
# GET ONE LOG
# ==========================================================

@router.get(
    "/{log_id}",
    response_model=LogResponse,
)
def get_log(
    log_id: int,
    db: Session = Depends(get_immo_db),
) -> LogResponse:
    """
    Return one execution log.
    """

    service: LogService = get_log_service(
        db
    )

    log = service.get_log(
        log_id
    )

    if log is None:

        raise HTTPException(

            status_code=404,

            detail="Log not found.",

        )
    
    print("=" * 80)
    print("ROUTER")
    print("business :", repr(log.business_knowledge))
    print("join     :", repr(log.join_knowledge))
    print("forbidden:", repr(log.forbidden_joins))
    print("semantic :", repr(log.semantic_context))
    print("=" * 80)

    return LogResponse(

        success=True,

        log=LogDetailsResponse(

            id=log.id,

            conversation_id=log.conversation_id,

            message_id=log.message_id,

            question=log.question,

            selected_tables=log.selected_tables,

            business_knowledge=log.business_knowledge,

            join_knowledge=log.join_knowledge,

            forbidden_joins=log.forbidden_joins,

            semantic_context=log.semantic_context,

            sql_patterns=log.sql_patterns,

            full_context=log.full_context,

            prompt=log.prompt,

            generated_sql=log.generated_sql,

            validated_sql=log.validated_sql,

            sql_result=log.sql_result,

            formatted_answer=log.formatted_answer,

            execution_time_ms=log.execution_time_ms,

            status=log.status,

            error_message=log.error_message,

            created_at=log.created_at,

        ),

    )