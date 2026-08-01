import re


class EntityDetector:
    """
    Detect entities contained in a natural language question.

    This class performs lexical extraction only.
    It never queries the database.
    """

    YEAR_PATTERN = r"\b(19\d{2}|20\d{2}|21\d{2})\b"

    YEAR_RANGE_PATTERN = (
        r"\b(19\d{2}|20\d{2}|21\d{2})\s*(?:-|à|to)\s*(19\d{2}|20\d{2}|21\d{2})\b"
    )

    NUMBER_PATTERN = r"\b\d+(?:[.,]\d+)?\b"

    PRODUCT_PATTERN = r"\bcpj[-\s]*([0-9]+)\b"

    MATERIAL_KEYWORDS = {

        "acier",
        "ciment",
        "beton",
        "béton",
        "sable",
        "gravette",
        "bois",
        "bitume",
        "cuivre",
        "marbre",
        "granit",
        "verre",
        "platre",
        "plâtre",
        "chaux",
        "aluminium",

    }

    REGION_KEYWORDS = {

        "tanger",
        "tetouan",
        "tétouan",
        "hoceima",
        "al hoceima",

        "oriental",

        "fes",
        "fès",

        "meknes",
        "meknès",

        "rabat",

        "sale",
        "salé",

        "kenitra",
        "kénitra",

        "beni mellal",
        "béni mellal",

        "khenifra",
        "khénifra",

        "casablanca",

        "settat",

        "marrakech",

        "safi",

        "draa",
        "drâa",

        "tafilalet",

        "souss",

        "massa",

        "guelmim",

        "laayoune",

        "dakhla",

    }

    def _normalize_text(
        self,
        question: str,
    ) -> str:
        """
        Normalize the user question before extraction.
        """
        return question.lower()

    def detect(
        self,
        question: str,
    ) -> dict:

        text = self._normalize_text(question)

        return {

            "years": self._extract_years(text),

            "year_ranges": self._extract_year_ranges(text),

            "numbers": self._extract_numbers(text),

            "regions": self._extract_keywords(
                text,
                self.REGION_KEYWORDS,
            ),

            "materials": self._extract_keywords(
                text,
                self.MATERIAL_KEYWORDS,
            ),

            "products": self._extract_products(text),

        }

    # -----------------------------------------------------

    def _extract_years(
        self,
        text: str,
    ) -> list[int]:

        return sorted({

            int(year)

            for year in re.findall(
                self.YEAR_PATTERN,
                text,
            )

        })

    # -----------------------------------------------------

    def _extract_year_ranges(
        self,
        text: str,
    ) -> list[tuple[int, int]]:

        return [
            (int(start), int(end))
            for start, end in re.findall(
                self.YEAR_RANGE_PATTERN,
                text,
            )
        ]

    # -----------------------------------------------------

    def _extract_numbers(
        self,
        text: str,
    ) -> list[float]:

        numbers = []

        for value in re.findall(
            self.NUMBER_PATTERN,
            text,
        ):

            try:

                numbers.append(
                    float(
                        value.replace(",", ".")
                    )
                )

            except ValueError:

                continue

        return numbers

    # -----------------------------------------------------

    def _extract_keywords(
        self,
        text: str,
        vocabulary: set[str],
    ) -> list[str]:

        return sorted({

            keyword

            for keyword in vocabulary

            if keyword in text

        })

    # -----------------------------------------------------

    def _extract_products(
        self,
        text: str,
    ) -> list[str]:

        return sorted({
            f"CPJ {value}"
            for value in re.findall(
                self.PRODUCT_PATTERN,
                text,
            )
        })