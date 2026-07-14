import re

from app.database.repositories.semantic_context_repository import (
    SemanticContextRepository,
)


class SemanticContextService:
    """
    Service responsible for retrieving the semantic
    database context associated with a user question.
    """

    def __init__(
        self,
        repository: SemanticContextRepository,
    ):

        self.repository = repository

    def build(
        self,
        question: str,
    ) -> list[dict]:
        """
        Build the semantic context used by the SQL Agent.
        """

        keywords = self._extract_keywords(
            question
        )

        columns = self.repository.search(
            keywords
        )

        context = []

        for column in columns:

            context.append(

                {

                    "table": column.table_name,

                    "column": column.column_name,

                    "semantic_type": column.semantic_type,

                    "examples": column.example_values,

                    "min_value": column.min_value,

                    "max_value": column.max_value,

                    "distinct_count": column.distinct_count,

                    "is_primary_key": column.is_primary_key,

                    "is_foreign_key": column.is_foreign_key,

                    "score": getattr(
                        column,
                        "semantic_score",
                        None,
                    ),

                }

            )

        return context

    def _extract_keywords(
        self,
        question: str,
    ) -> list[str]:
        """
        Extract meaningful keywords from a natural language question.
        """

        question = question.lower()

        words = re.findall(
            r"[a-zA-ZÀ-ÿ0-9]+",
            question,
        )

        stop_words = {

            "le",
            "la",
            "les",
            "de",
            "des",
            "du",
            "dans",
            "sur",
            "sous",
            "pour",
            "par",
            "avec",
            "sans",
            "et",
            "ou",
            "un",
            "une",
            "est",
            "sont",
            "quel",
            "quelle",
            "quels",
            "quelles",
            "donne",
            "donner",
            "montre",
            "affiche",
            "liste",
            "voir",
            "afficher",
            "peux",
            "peut",
            "avoir",
            "faire",
            "tous",
            "toutes",
            "entre",
            "vers",
            "chez",
            "plus",
            "moins",
            "combien",
            "moi",
        }

        keywords = []

        for word in words:

            word = word.strip()

            if len(word) < 2:
                continue

            if word in stop_words:
                continue

            keywords.append(word)

        keywords = list(
            dict.fromkeys(
                keywords
            )
        )

        return keywords