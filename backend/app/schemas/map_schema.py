from pydantic import BaseModel


# ==========================================================
# Région
# ==========================================================

class RegionResponse(BaseModel):
    id_region: int
    code_region: str
    nom_region: str
    nom_region_ar: str | None = None
    code_iso: str | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Province
# ==========================================================

class ProvinceResponse(BaseModel):
    id_province: int
    nom_province: str

    class Config:
        from_attributes = True


# ==========================================================
# Région détaillée
# ==========================================================

class RegionDetailsResponse(BaseModel):
    id_region: int
    code_region: str
    nom_region: str
    nom_region_ar: str | None = None
    code_iso: str | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Cartes statistiques
# ==========================================================

class RegionStatisticsResponse(BaseModel):
    region: str
    nombre_provinces: int
    prix_moyen: float | None = None
    indice_moyen: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Historique des prix
# ==========================================================

class PriceHistoryResponse(BaseModel):
    annee: int
    materiau: str
    prix_moyen: float | None = None
    indice: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Habitat
# ==========================================================

class HousingStatisticsResponse(BaseModel):
    annee: int
    type_habitat: str
    type_indicateur: str
    montant_mad: float | None = None
    indice: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Recherche
# ==========================================================

class RegionSearchResponse(BaseModel):
    id_region: int
    nom_region: str

    class Config:
        from_attributes = True


# ==========================================================
# Matériaux
# ==========================================================

class MaterialResponse(BaseModel):
    id: int
    nom: str

    class Config:
        from_attributes = True


# ==========================================================
# Années disponibles
# ==========================================================

class YearResponse(BaseModel):
    annee: int

    class Config:
        from_attributes = True


# ==========================================================
# Analyse des prix
# ==========================================================

class PriceAnalysisRow(BaseModel):
    annee: int
    materiau: str
    prix_moyen: float | None = None
    indice: float | None = None

    class Config:
        from_attributes = True


class PriceAnalysisResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    rows: list[PriceAnalysisRow]

    class Config:
        from_attributes = True


# ==========================================================
# Analyse Habitat
# ==========================================================

class HousingAnalysisRow(BaseModel):
    annee: int
    type_habitat: str
    type_indicateur: str
    montant_mad: float | None = None
    indice: float | None = None

    class Config:
        from_attributes = True


class HousingAnalysisResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    rows: list[HousingAnalysisRow]

    class Config:
        from_attributes = True