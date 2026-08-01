from app.agents.sql_agent.patterns.sql_pattern_repository import (
    SQLPatternRepository,
)
from app.agents.sql_agent.patterns.sql_pattern_selector import (
    SQLPatternSelector,
)


class SQLPatterns:
    """
    Facade responsible for retrieving SQL patterns.

    The SQL Agent communicates only with this class,
    without knowing how SQL patterns are stored
    or selected.
    """

    def __init__(
        self,
        repository: SQLPatternRepository | None = None,
        selector: SQLPatternSelector | None = None,
    ):
        self.repository = (
            repository
            or SQLPatternRepository()
        )

        self.selector = (
            selector
            or SQLPatternSelector(
                repository=self.repository,
            )
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get_patterns(
        self,
        question: str,
        selection: dict,
    ) -> list[dict]:
        """
        Return the SQL patterns that best match the
        user question and the detected business context.
        """

        return self.selector.select(
            question=question,
            selection=selection,
        )