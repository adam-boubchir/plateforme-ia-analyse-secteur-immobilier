from __future__ import annotations

import re
from typing import Final

from app.services.semantic_metadata.semantic_keyword_service import (
    SemanticKeywordService,
)

__all__ = ["SemanticTypeDetector"]

CAMEL_CASE_PATTERN: Final[str] = r"([a-z])([A-Z])"


class SemanticTypeDetector:
    """
    Detect the semantic type of a table or column name.
    """

    def __init__(
        self,
        keyword_service: SemanticKeywordService,
    ) -> None:
        self.keyword_service = keyword_service

    # ------------------------------------------------------------------
    # PUBLIC
    # ------------------------------------------------------------------

    def detect(
        self,
        text: str,
    ) -> str | None:
        """
        Detect the semantic type associated with a column or table name.
        """

        best_score = -1
        best_semantic: str | None = None

        for token in self._tokenize(text):

            keyword = self.keyword_service.find(token)

            if keyword is None:
                continue

            score = keyword["score"]

            if score <= best_score:
                continue

            best_score = score
            best_semantic = keyword["semantic_type"]

        return best_semantic

    # ------------------------------------------------------------------
    # PRIVATE
    # ------------------------------------------------------------------

    def _tokenize(
        self,
        text: str,
    ) -> list[str]:
        """
        Split a database identifier into normalized tokens.

        Examples
        --------
        nom_region
            -> ["nom", "region"]

        prixMoyen
            -> ["prix", "moyen"]

        id-region
            -> ["id", "region"]
        """

        normalized = re.sub(
            CAMEL_CASE_PATTERN,
            r"\1 \2",
            text,
        )

        normalized = (
            normalized
            .replace("_", " ")
            .replace("-", " ")
        )

        return [
            token.casefold()
            for token in normalized.split()
            if token.strip()
        ]