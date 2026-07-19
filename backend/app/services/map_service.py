from sqlalchemy.orm import Session

from app.database.repositories.map_repository import MapRepository


class MapService:

    def __init__(
        self,
        db: Session,
    ):
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
    # Statistiques
    # ==========================================================

    def get_region_statistics(
        self,
        region_id: int,
    ):
        return self.repository.get_region_statistics(region_id)

    # ==========================================================
    # Evolution des prix
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