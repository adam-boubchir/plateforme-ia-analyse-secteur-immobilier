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
# Informations Région
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
# Evolution des prix
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