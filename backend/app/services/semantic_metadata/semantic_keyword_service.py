from app.database.repositories.semantic_keyword_repository import (
    SemanticKeywordRepository,
)


class SemanticKeywordService:
    """
    Service responsible for loading semantic keywords.
    """

    def __init__(
        self,
        repository: SemanticKeywordRepository,
    ):

        self.repository = repository

        self._keywords = None

    def load(self) -> None:
        """
        Load all semantic keywords into memory.
        """

        self._keywords = self.repository.get_all()

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

        word = word.lower()

        for keyword in self.get_all():

            if keyword["keyword"] == word:

                return keyword

        return None