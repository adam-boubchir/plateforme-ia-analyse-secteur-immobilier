from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.entities.region import Region
from app.database.entities.province_prefecture import ProvincePrefecture
from app.database.entities.fact_indicateur_habitat import FactIndicateurHabitat
from app.database.entities.fact_prix_indices import FactPrixIndices
from app.database.entities.niveau_materiau import NiveauMateriau
from app.database.entities.type_habitat import TypeHabitat
from app.database.entities.envergure_habitat import EnvergureHabitat

from app.database.repositories.base_repository import BaseRepository


class MapRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    # ==========================================================
    # Régions
    # ==========================================================

    def get_regions(self):
        """
        Retourne toutes les régions.
        """
        return (
            self.db.query(Region)
            .order_by(Region.nom_region.asc())
            .all()
        )

    def get_region_by_code(
        self,
        code_iso: str,
    ):
        """
        Retourne une région à partir de son code ISO.
        Exemple : MA-06
        """

        return (
            self.db.query(Region)
            .filter(
                Region.code_iso == code_iso
            )
            .first()
        )

    def get_region(
        self,
        region_id: int,
    ):
        """
        Retourne une région par son identifiant.
        """

        return (
            self.db.query(Region)
            .filter(
                Region.id_region == region_id
            )
            .first()
        )

    def search_regions(
        self,
        keyword: str,
    ):
        """
        Recherche une région par son nom ou son code.
        """

        keyword = keyword.strip()

        return (
            self.db.query(Region)
            .filter(
                (Region.nom_region.ilike(f"%{keyword}%"))
                | (Region.code_region.ilike(f"%{keyword}%"))
            )
            .order_by(
                Region.nom_region.asc()
            )
            .all()
        )

    # ==========================================================
    # Statistiques
    # ==========================================================

    def get_region_statistics(
        self,
        region_id: int,
    ):
        """
        Cartes statistiques.
        """

        region = self.get_region(region_id)

        if region is None:
            return None

        nombre_provinces = (
            self.db.query(
                func.count(ProvincePrefecture.id_province)
            )
            .filter(
                ProvincePrefecture.id_region == region_id
            )
            .scalar()
        )

        prix = (
            self.db.query(
                func.avg(FactPrixIndices.prix_moyen),
                func.avg(FactPrixIndices.indice),
            )
            .filter(
                FactPrixIndices.id_region == region_id
            )
            .first()
        )

        return {
            "region": region.nom_region,
            "nombre_provinces": nombre_provinces or 0,
            "prix_moyen": float(prix[0]) if prix and prix[0] is not None else None,
            "indice_moyen": float(prix[1]) if prix and prix[1] is not None else None,
        }

    # ==========================================================
    # Prix
    # ==========================================================

    def get_price_history(
        self,
        region_id: int,
    ):
        """
        Evolution des prix.
        """

        return (
            self.db.query(
                FactPrixIndices.annee.label("annee"),
                NiveauMateriau.nom.label("materiau"),
                FactPrixIndices.prix_moyen.label("prix_moyen"),
                FactPrixIndices.indice.label("indice"),
            )
            .join(
                NiveauMateriau,
                FactPrixIndices.id_niveau_mat
                == NiveauMateriau.id
            )
            .filter(
                FactPrixIndices.id_region == region_id
            )
            .order_by(
                FactPrixIndices.annee.asc()
            )
            .all()
        )

    # ==========================================================
    # Habitat
    # ==========================================================

    def get_housing_statistics(
        self,
        region_id: int,
    ):
        """
        Evolution habitat.
        """

        return (
            self.db.query(
                FactIndicateurHabitat.annee.label("annee"),
                TypeHabitat.nom_type.label("type_habitat"),
                FactIndicateurHabitat.type_indicateur.label("type_indicateur"),
                FactIndicateurHabitat.montant_mad.label("montant_mad"),
                FactIndicateurHabitat.indice.label("indice"),
            )
            .join(
                TypeHabitat,
                FactIndicateurHabitat.id_type_habitat
                == TypeHabitat.id_type_habitat,
            )
            .filter(
                FactIndicateurHabitat.id_region == region_id
            )
            .order_by(
                FactIndicateurHabitat.annee.asc()
            )
            .all()
        )