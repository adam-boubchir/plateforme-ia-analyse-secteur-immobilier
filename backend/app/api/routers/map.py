from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_ministry_db
from app.schemas.map_schema import (
    HousingStatisticsResponse,
    PriceHistoryResponse,
    RegionResponse,
    RegionStatisticsResponse,
)
from app.services.map_service import MapService

router = APIRouter(
    prefix="/api/map",
    tags=["Map"],
)


def _get_region_or_404(service: MapService, code_iso: str):
    region = service.get_region_by_code(code_iso)

    if region is None:
        raise HTTPException(
            status_code=404,
            detail="Région introuvable",
        )

    return region


# ==========================================================
# Régions
# ==========================================================

@router.get(
    "/regions",
    response_model=list[RegionResponse],
)
def get_regions(
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    return service.get_regions()


@router.get(
    "/regions/{region_id}",
    response_model=RegionResponse,
)
def get_region(
    region_id: int,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)

    region = service.get_region(region_id)

    if region is None:
        raise HTTPException(
            status_code=404,
            detail="Région introuvable",
        )

    return region


@router.get(
    "/regions/code/{code_iso}",
    response_model=RegionResponse,
)
def get_region_by_code(
    code_iso: str,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    return _get_region_or_404(service, code_iso)


# ==========================================================
# Statistiques
# ==========================================================

@router.get(
    "/regions/{region_id}/statistics",
    response_model=RegionStatisticsResponse,
)
def get_region_statistics(
    region_id: int,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    return service.get_region_statistics(region_id)


@router.get(
    "/regions/code/{code_iso}/statistics",
    response_model=RegionStatisticsResponse,
)
def get_region_statistics_by_code(
    code_iso: str,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    region = _get_region_or_404(service, code_iso)

    return service.get_region_statistics(region.id_region)


# ==========================================================
# Prix
# ==========================================================

@router.get(
    "/regions/{region_id}/prices",
    response_model=list[PriceHistoryResponse],
)
def get_price_history(
    region_id: int,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    return service.get_price_history(region_id)


@router.get(
    "/regions/code/{code_iso}/prices",
    response_model=list[PriceHistoryResponse],
)
def get_price_history_by_code(
    code_iso: str,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    region = _get_region_or_404(service, code_iso)

    return service.get_price_history(region.id_region)


# ==========================================================
# Habitat
# ==========================================================

@router.get(
    "/regions/{region_id}/housing",
    response_model=list[HousingStatisticsResponse],
)
def get_housing_statistics(
    region_id: int,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    return service.get_housing_statistics(region_id)


@router.get(
    "/regions/code/{code_iso}/housing",
    response_model=list[HousingStatisticsResponse],
)
def get_housing_statistics_by_code(
    code_iso: str,
    db: Session = Depends(get_ministry_db),
):
    service = MapService(db)
    region = _get_region_or_404(service, code_iso)

    return service.get_housing_statistics(region.id_region)