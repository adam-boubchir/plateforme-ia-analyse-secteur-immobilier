from sqlalchemy import text
from sqlalchemy.orm import Session


class ValueRetriever:
    """
    Retrieve useful business values from the database.

    This class enriches the prompt with representative values
    corresponding to the detected entities.
    """

    MAX_VALUES = 20

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def retrieve(
        self,
        entities: dict,
    ) -> str:
        """
        Build additional business context from detected entities.
        """

        context = []

        if entities.get("regions"):

            context.extend(
                self._get_regions()
            )

        if entities.get("materials"):

            context.extend(
                self._get_materials()
            )

        if entities.get("products"):

            context.extend(
                self._get_products(
                    entities["products"]
                )
            )

        if entities.get("years"):

            context.append("")
            context.append("REQUESTED YEARS")
            context.append("----------------")

            for year in entities["years"]:

                context.append(
                    str(year)
                )

            context.append("")

        return "\n".join(context)

    # =====================================================
    # Regions
    # =====================================================

    def _get_regions(
        self,
    ) -> list[str]:

        sql = text(
            f"""
            SELECT TOP ({self.MAX_VALUES})
                nom_region
            FROM REGION
            ORDER BY nom_region
            """
        )

        rows = self.db.execute(
            sql
        ).fetchall()

        context = []

        context.append("")
        context.append("KNOWN REGIONS")
        context.append("----------------")

        for row in rows:

            context.append(
                row.nom_region
            )

        context.append("")

        return context

    # =====================================================
    # Materials
    # =====================================================

    def _get_materials(
        self,
    ) -> list[str]:

        sql = text(
            f"""
            SELECT DISTINCT TOP ({self.MAX_VALUES})
                nom
            FROM NIVEAU_MATERIAU
            WHERE nom IS NOT NULL
            ORDER BY nom
            """
        )

        rows = self.db.execute(
            sql
        ).fetchall()

        context = []

        context.append("")
        context.append("KNOWN MATERIALS")
        context.append("----------------")

        for row in rows:

            context.append(
                row.nom
            )

        context.append("")

        return context

    # =====================================================
    # Products
    # =====================================================

    def _get_products(
        self,
        products: list[str],
    ) -> list[str]:

        context = []

        context.append("")
        context.append("MATCHING PRODUCTS")
        context.append("----------------")

        for product in products:

            sql = text(
                """
                SELECT DISTINCT nom
                FROM NIVEAU_MATERIAU
                WHERE nom LIKE :value
                ORDER BY nom
                """
            )

            rows = self.db.execute(
                sql,
                {
                    "value": f"%{product}%"
                }
            ).fetchall()

            for row in rows:

                context.append(
                    row.nom
                )

        context.append("")

        return context