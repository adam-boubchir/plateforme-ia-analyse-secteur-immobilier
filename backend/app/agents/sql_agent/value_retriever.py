from sqlalchemy import text
from sqlalchemy.orm import Session


class ValueRetriever:
    """
    Retrieve useful business values from the database.

    This class enriches the SQL prompt with representative
    business values extracted from the database.
    """

    MAX_VALUES = 20

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def retrieve(
        self,
        entities: dict,
    ) -> str:
        """
        Build additional business context.
        """

        sections = []

        if entities.get("regions"):
            sections.extend(
                self._get_regions()
            )

        if entities.get("materials"):
            sections.extend(
                self._get_materials()
            )

        if entities.get("products"):
            sections.extend(
                self._get_products(
                    entities["products"]
                )
            )

        if entities.get("years"):
            sections.extend(
                self._format_years(
                    entities["years"]
                )
            )

        return "\n".join(sections)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _execute(
        self,
        sql,
        params: dict | None = None,
    ):
        """
        Execute a SQL query.
        """

        return self.db.execute(
            sql,
            params or {},
        ).fetchall()

    def _build_section(
        self,
        title: str,
        values: list[str],
    ) -> list[str]:
        """
        Build one formatted context section.
        """

        if not values:
            return []

        return [
            "",
            title,
            "----------------",
            *values,
            "",
        ]

    # ==========================================================
    # Regions
    # ==========================================================

    def _get_regions(
        self,
    ) -> list[str]:

        rows = self._execute(
            text(
                f"""
                SELECT TOP ({self.MAX_VALUES})
                    nom_region
                FROM REGION
                ORDER BY nom_region
                """
            )
        )

        return self._build_section(
            "KNOWN REGIONS",
            [
                row.nom_region
                for row in rows
            ],
        )

    # ==========================================================
    # Materials
    # ==========================================================

    def _get_materials(
        self,
    ) -> list[str]:

        rows = self._execute(
            text(
                f"""
                SELECT DISTINCT TOP ({self.MAX_VALUES})
                    nom
                FROM NIVEAU_MATERIAU
                WHERE nom IS NOT NULL
                ORDER BY nom
                """
            )
        )

        return self._build_section(
            "KNOWN MATERIALS",
            [
                row.nom
                for row in rows
            ],
        )

    # ==========================================================
    # Products
    # ==========================================================

    def _get_products(
        self,
        products: list[str],
    ) -> list[str]:

        values = []

        sql = text(
            """
            SELECT DISTINCT nom
            FROM NIVEAU_MATERIAU
            WHERE nom LIKE :value
            ORDER BY nom
            """
        )

        for product in products:

            rows = self._execute(
                sql,
                {
                    "value": f"%{product}%"
                },
            )

            values.extend(
                row.nom
                for row in rows
            )

        values = sorted(
            set(values)
        )

        return self._build_section(
            "MATCHING PRODUCTS",
            values,
        )

    # ==========================================================
    # Years
    # ==========================================================

    def _format_years(
        self,
        years: list[int],
    ) -> list[str]:

        return self._build_section(
            "REQUESTED YEARS",
            [
                str(year)
                for year in years
            ],
        )