from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_ministry_db

from app.schemas.map_schema import (
    RegionResponse,
    ProvinceResponse,
    RegionStatisticsResponse,
    PriceHistoryResponse,
    HousingStatisticsResponse,
    PriceAnalysisResponse,
    MaterialResponse,
    YearResponse,
    HousingAnalysisResponse,
)

from app.schemas.analysis_schema import (
    AnalysisRequest,
)

from app.services.map_service import MapService

router = APIRouter(
    prefix="/api/map",
    tags=["Map"],
)


# ==========================================================
# Helpers
# ==========================================================

def get_service(
    db: Session = Depends(get_ministry_db),
) -> MapService:
    return MapService(db)


def get_region_or_404(
    service: MapService,
    code_iso: str,
):
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
    service: MapService = Depends(get_service),
):
    return service.get_regions()


@router.get(
    "/regions/{region_id}",
    response_model=RegionResponse,
)
def get_region(
    region_id: int,
    service: MapService = Depends(get_service),
):
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
    service: MapService = Depends(get_service),
):
    return get_region_or_404(
        service,
        code_iso,
    )


# ==========================================================
# Provinces
# ==========================================================

@router.get(
    "/regions/code/{code_iso}/provinces",
    response_model=list[ProvinceResponse],
)
def get_provinces(
    code_iso: str,
    service: MapService = Depends(get_service),
):
    region = get_region_or_404(
        service,
        code_iso,
    )

    return service.get_provinces_by_region(
        region.id_region
    )


# ==========================================================
# Statistiques
# ==========================================================

@router.get(
    "/regions/code/{code_iso}/statistics",
    response_model=RegionStatisticsResponse,
)
def get_statistics(
    code_iso: str,
    service: MapService = Depends(get_service),
):
    region = get_region_or_404(
        service,
        code_iso,
    )

    return service.get_region_statistics(
        region.id_region
    )


# ==========================================================
# Historique des prix
# ==========================================================

@router.get(
    "/regions/code/{code_iso}/prices",
    response_model=list[PriceHistoryResponse],
)
def get_prices(
    code_iso: str,
    service: MapService = Depends(get_service),
):
    region = get_region_or_404(
        service,
        code_iso,
    )

    return service.get_price_history(
        region.id_region
    )


# ==========================================================
# Habitat
# ==========================================================

@router.get(
    "/regions/code/{code_iso}/housing",
    response_model=list[HousingStatisticsResponse],
)
def get_housing(
    code_iso: str,
    service: MapService = Depends(get_service),
):
    region = get_region_or_404(
        service,
        code_iso,
    )

    return service.get_housing_statistics(
        region.id_region
    )

# ==========================================================
# Matériaux
# ==========================================================

@router.get(
    "/materials",
    response_model=list[MaterialResponse],
)
def get_materials(
    service: MapService = Depends(get_service),
):
    return service.get_materials() 


# ==========================================================
# Années
# ==========================================================

@router.get(
    "/years",
    response_model=list[YearResponse],
)
def get_available_years(
    service: MapService = Depends(get_service),
):
    return service.get_available_years()


# ==========================================================
# Analyse
# ==========================================================

from app.schemas.analysis_schema import (
    AnalysisRequest,
    AnalysisResponse,
)

@router.post("/analysis")
def analyze(
    request: AnalysisRequest,
    service: MapService = Depends(get_service),
):

    if request.analysis_type == "prices":
        return service.analyze_prices(
            region_id=request.region_id,
            province_id=request.province_id,
            material_id=request.material_id,
            year=request.year,
            page=request.page,
            page_size=request.page_size,
        )

    if request.analysis_type == "housing":
        return service.analyze_housing(
            region_id=request.region_id,
            province_id=request.province_id,
            year=request.year,
            page=request.page,
            page_size=request.page_size,
        )

    raise HTTPException(
        status_code=400,
        detail="L'analyse 'both' n'est pas encore supportée."
    )