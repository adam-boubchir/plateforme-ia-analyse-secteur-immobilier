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
    
    # ==========================================================
    # Provinces
    # ==========================================================

    def get_provinces_by_region(
        self,
        region_id: int,
    ):
        """
        Retourne toutes les provinces/préfectures d'une région.
        """

        return (
            self.db.query(
                ProvincePrefecture.id_province,
                ProvincePrefecture.nom_province,
            )
            .filter(
                ProvincePrefecture.id_region == region_id
            )
            .order_by(
                ProvincePrefecture.nom_province.asc()
            )
            .all()
        )
    
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
        """
        Analyse des prix avec filtres et pagination.
        """

        query = self._build_price_query(
            region_id=region_id,
            province_id=province_id,
            material_id=material_id,
            year=year,
        )

        total = query.order_by(None).count()

        rows = [
            dict(row._mapping)
            for row in (
                query.order_by(
                    FactPrixIndices.annee.desc(),
                    NiveauMateriau.nom.asc(),
                )
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
        ]

        print(type(rows))
        print(type(rows[0]))
        print(rows[0])

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (
                (total + page_size - 1) // page_size
                if page_size
                else 1
            ),
            "rows": rows,
        }

    def analyze_housing(
        self,
        region_id: int,
        province_id: int | None = None,
        year: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        """
        Analyse Habitat avec filtres et pagination.
        """

        query = self._build_housing_query(
            region_id=region_id,
            province_id=province_id,
            year=year,
        )

        total = query.order_by(None).count()

        rows = [
            dict(row._mapping)
            for row in (
                query.order_by(
                    FactIndicateurHabitat.annee.desc(),
                    TypeHabitat.nom_type.asc(),
                )
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
        ]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (
                (total + page_size - 1) // page_size
                if page_size
                else 1
            ),
            "rows": rows,
        }

    def _build_price_query(
        self,
        region_id: int,
        province_id: int | None = None,
        material_id: int | None = None,
        year: int | None = None,
    ):
        query = (
            self.db.query(
                FactPrixIndices.annee.label("annee"),
                NiveauMateriau.nom.label("materiau"),
                FactPrixIndices.prix_moyen.label("prix_moyen"),
                FactPrixIndices.indice.label("indice"),
            )
            .join(
                NiveauMateriau,
                FactPrixIndices.id_niveau_mat == NiveauMateriau.id,
            )
            .filter(
                FactPrixIndices.id_region == region_id
            )
        )

        if province_id is not None:
            query = query.filter(
                FactPrixIndices.id_province == province_id
            )

        if material_id is not None:
            query = query.filter(
                FactPrixIndices.id_niveau_mat == material_id
            )

        if year is not None:
            query = query.filter(
                FactPrixIndices.annee == year
            )

        return query

    def _build_housing_query(
        self,
        region_id: int,
        province_id: int | None = None,
        year: int | None = None,
    ):
        query = (
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
        )

        if province_id is not None:
            query = query.filter(
                FactIndicateurHabitat.id_province == province_id
            )

        if year is not None:
            query = query.filter(
                FactIndicateurHabitat.annee == year
            )

        return query

    def get_available_years(self):
        return (
            self.db.query(FactPrixIndices.annee)
            .distinct()
            .order_by(FactPrixIndices.annee.desc())
            .all()
        )


    def get_materials(self):
        return (
            self.db.query(
                NiveauMateriau.id,
                NiveauMateriau.nom,
            )
            .order_by(
                NiveauMateriau.nom.asc()
            )
            .all()
        )