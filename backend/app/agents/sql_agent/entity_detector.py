from __future__ import annotations

import re
from typing import TypedDict

__all__ = ("EntityDetector",)


class DetectedEntities(TypedDict):
    """
    Structured entities extracted from a user question.
    """

    years: list[int]
    year_ranges: list[tuple[int, int]]
    numbers: list[float]
    regions: list[str]
    materials: list[str]
    products: list[str]


class EntityDetector:
    """
    Detect structured entities contained in a natural-language question.

    Responsibilities
    ----------------
    - Detect years.
    - Detect year ranges.
    - Detect numeric values.
    - Detect Moroccan regions.
    - Detect construction materials.
    - Detect construction product identifiers.
    """

    _YEAR_PATTERN = re.compile(
        r"\b(19\d{2}|20\d{2}|21\d{2})\b",
    )

    _YEAR_RANGE_PATTERN = re.compile(
        r"\b(19\d{2}|20\d{2}|21\d{2})\s*(?:-|à|to)\s*(19\d{2}|20\d{2}|21\d{2})\b",
    )

    _NUMBER_PATTERN = re.compile(
        r"\b\d+(?:[.,]\d+)?\b",
    )

    _PRODUCT_PATTERN = re.compile(
        r"\bcpj[-\s]*([0-9]+)\b",
    )

    _MATERIAL_KEYWORDS: frozenset[str] = frozenset(
        {
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
    )

    _REGION_KEYWORDS: frozenset[str] = frozenset(
        {
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
    )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def detect(
        self,
        *,
        question: str,
    ) -> DetectedEntities:
        """
        Detect structured entities from a natural-language question.

        Args:
            question: User question.

        Returns:
            Dictionary containing every detected entity.
        """

        text = self._normalize_text(
            question=question,
        )

        entities: DetectedEntities = {
            "years": self._extract_years(
                text=text,
            ),
            "year_ranges": self._extract_year_ranges(
                text=text,
            ),
            "numbers": self._extract_numbers(
                text=text,
            ),
            "regions": self._extract_keywords(
                text=text,
                vocabulary=self._REGION_KEYWORDS,
            ),
            "materials": self._extract_keywords(
                text=text,
                vocabulary=self._MATERIAL_KEYWORDS,
            ),
            "products": self._extract_products(
                text=text,
            ),
        }

        return entities

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _normalize_text(
        *,
        question: str,
    ) -> str:
        """Normalize the user question."""

        normalized_question = question.casefold().strip()

        return normalized_question

    @classmethod
    def _extract_years(
        cls,
        *,
        text: str,
    ) -> list[int]:
        """Extract unique years."""

        years = sorted(
            {
                int(year)
                for year in cls._YEAR_PATTERN.findall(text)
            }
        )

        return years

    @classmethod
    def _extract_year_ranges(
        cls,
        *,
        text: str,
    ) -> list[tuple[int, int]]:
        """Extract year ranges."""

        year_ranges = [
            (int(start), int(end))
            for start, end in cls._YEAR_RANGE_PATTERN.findall(text)
        ]

        return year_ranges

    @classmethod
    def _extract_numbers(
        cls,
        *,
        text: str,
    ) -> list[float]:
        """Extract numeric values."""

        numbers: list[float] = []

        for value in cls._NUMBER_PATTERN.findall(text):
            try:
                numbers.append(
                    float(
                        value.replace(",", "."),
                    )
                )
            except ValueError:
                continue

        return numbers

    @staticmethod
    def _extract_keywords(
        *,
        text: str,
        vocabulary: frozenset[str],
    ) -> list[str]:
        """Extract keywords from a predefined vocabulary."""

        keywords = sorted(
            {
                keyword
                for keyword in vocabulary
                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text,
                )
            }
        )

        return keywords

    @classmethod
    def _extract_products(
        cls,
        *,
        text: str,
    ) -> list[str]:
        """Extract construction product identifiers."""

        products = sorted(
            {
                f"CPJ {value}"
                for value in cls._PRODUCT_PATTERN.findall(text)
            }
        )

        return products