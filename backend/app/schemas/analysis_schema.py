from pydantic import BaseModel, Field
from typing import Literal


# ==========================================================
# Request
# ==========================================================

class AnalysisRequest(BaseModel):
    analysis_type: Literal[
        "prices",
        "housing",
        "both",
    ]

    region_id: int

    province_id: int | None = None

    material_id: int | None = None

    year: int | None = None

    page: int = Field(default=1, ge=1)

    page_size: int = Field(default=20, ge=1, le=100)


# ==========================================================
# Dashboard
# ==========================================================

class DashboardSummary(BaseModel):
    nombre_provinces: int
    prix_moyen: float | None = None
    indice_moyen: float | None = None


# ==========================================================
# Price Row
# ==========================================================

class PriceAnalysisRow(BaseModel):
    annee: int

    materiau: str

    prix_moyen: float | None = None

    indice: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Housing Row
# ==========================================================

class HousingAnalysisRow(BaseModel):

    annee: int

    type_habitat: str

    type_indicateur: str

    montant_mad: float | None = None

    indice: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Pagination
# ==========================================================

class Pagination(BaseModel):

    total: int

    page: int

    page_size: int

    total_pages: int


# ==========================================================
# Response
# ==========================================================

class AnalysisResponse(BaseModel):

    dashboard: DashboardSummary | None = None

    prices: list[PriceAnalysisRow] = []

    housing: list[HousingAnalysisRow] = []

    pagination: Pagination | None = None