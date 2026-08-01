from __future__ import annotations

from app.database.repositories.semantic_keyword_repository import (
    SemanticKeywordRepository,
)

__all__ = ["SemanticKeywordService"]


class SemanticKeywordService:
    """
    Service responsible for loading semantic keywords.
    """

    def __init__(
        self,
        repository: SemanticKeywordRepository,
    ) -> None:
        self.repository = repository

        self._keywords: list[dict] | None = None
        self._keyword_index: dict[str, dict] | None = None

    # ------------------------------------------------------------------
    # PUBLIC
    # ------------------------------------------------------------------

    def load(self) -> None:
        """
        Load all semantic keywords into memory.
        """

        self._keywords = self.repository.get_all()

        self._keyword_index = {
            keyword["keyword"].casefold(): keyword
            for keyword in self._keywords
        }

    def get_all(self) -> list[dict]:
        """
        Return all loaded keywords.
        """

        if self._keywords is None:
            self.load()

        return self._keywords

    def find(
        self,
        word: str,
    ) -> dict | None:
        """
        Find one keyword.
        """

        if self._keyword_index is None:
            self.load()

        return self._keyword_index.get(
            word.casefold()
        )