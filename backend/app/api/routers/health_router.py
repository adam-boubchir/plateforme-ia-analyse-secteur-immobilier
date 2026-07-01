from fastapi import APIRouter

from app.api.models.health_models import (
    HealthResponse,
)

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    """
    Health check endpoint.
    """

    return HealthResponse(
        status="ok"
    )