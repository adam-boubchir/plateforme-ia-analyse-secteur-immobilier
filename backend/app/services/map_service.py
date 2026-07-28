from sqlalchemy.orm import Session

from app.database.repositories.map_repository import MapRepository


class MapService:

    def __init__(self, db: Session):
        self.repository = MapRepository(db)

    # ==========================================================
    # Régions
    # ==========================================================

    def get_regions(self):
        return self.repository.get_regions()

    def get_region(
        self,
        region_id: int,
    ):
        return self.repository.get_region(region_id)

    def get_region_by_code(
        self,
        code_iso: str,
    ):
        return self.repository.get_region_by_code(code_iso)

    def search_regions(
        self,
        keyword: str,
    ):
        return self.repository.search_regions(keyword)

    # ==========================================================
    # Provinces
    # ==========================================================

    def get_provinces_by_region(
        self,
        region_id: int,
    ):
        return self.repository.get_provinces_by_region(region_id)

    # ==========================================================
    # Statistiques
    # ==========================================================

    def get_region_statistics(
        self,
        region_id: int,
    ):
        return self.repository.get_region_statistics(region_id)

    # ==========================================================
    # Prix
    # ==========================================================

    def get_price_history(
        self,
        region_id: int,
    ):
        return self.repository.get_price_history(region_id)

    # ==========================================================
    # Habitat
    # ==========================================================

    def get_housing_statistics(
        self,
        region_id: int,
    ):
        return self.repository.get_housing_statistics(region_id)

    # ==========================================================
    # Analyse
    # ==========================================================

    def analyze_prices(
        self,
        region_id: int,
        province_id: int | None = None,
        material_id: int | None = None,
        year: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        return self.repository.analyze_prices(
            region_id=region_id,
            province_id=province_id,
            material_id=material_id,
            year=year,
            page=page,
            page_size=page_size,
        )

    def analyze_housing(
        self,
        region_id: int,
        province_id: int | None = None,
        year: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        return self.repository.analyze_housing(
            region_id=region_id,
            province_id=province_id,
            year=year,
            page=page,
            page_size=page_size,
        )

    # ==========================================================
    # Filtres
    # ==========================================================

    def get_materials(self):
        return self.repository.get_materials()

    def get_available_years(self):
        return self.repository.get_available_years()