import re

from app.services.semantic_metadata.semantic_keyword_service import (
    SemanticKeywordService,
)


class SemanticTypeDetector:
    """
    Detect the semantic type of a table or column.
    """

    def __init__(
        self,
        keyword_service: SemanticKeywordService,
    ):

        self.keyword_service = keyword_service

    def detect(
        self,
        text: str,
    ) -> str | None:
        """
        Detect the semantic type.

        Example:

        nom_region
            ->
        REGION

        prix_moyen
            ->
        MEASURE
        """

        tokens = self._tokenize(text)

        best_score = -1

        best_semantic = None

        for token in tokens:

            keyword = self.keyword_service.find(
                token
            )

            if keyword is None:
                continue

            if keyword["score"] > best_score:

                best_score = keyword["score"]

                best_semantic = keyword[
                    "semantic_type"
                ]

        return best_semantic

    def _tokenize(
        self,
        text: str,
    ) -> list[str]:
        """
        Split a name into tokens.

        Examples

        nom_region
            ->
        ["nom","region"]

        prixMoyen
            ->
        ["prix","moyen"]

        id_region
            ->
        ["id","region"]
        """

        text = re.sub(
            r"([a-z])([A-Z])",
            r"\1 \2",
            text,
        )

        text = text.replace("_", " ")

        text = text.replace("-", " ")

        tokens = []

        for token in text.split():

            token = token.strip().lower()

            if token:

                tokens.append(token)

        return tokens