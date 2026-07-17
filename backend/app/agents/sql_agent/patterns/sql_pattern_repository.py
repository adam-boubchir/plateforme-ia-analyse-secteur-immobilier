from app.agents.sql_agent.patterns.aggregate_patterns import (
    AggregatePatterns,
)

from app.agents.sql_agent.patterns.ranking_patterns import (
    RankingPatterns,
)

from app.agents.sql_agent.patterns.comparison_patterns import (
    ComparisonPatterns,
)

from app.agents.sql_agent.patterns.evolution_patterns import (
    EvolutionPatterns,
)

from app.agents.sql_agent.patterns.geographic_patterns import (
    GeographicPatterns,
)

from app.agents.sql_agent.patterns.statistical_patterns import (
    StatisticalPatterns,
)


class SQLPatternRepository:
    """
    Central repository containing every SQL pattern.

    This class loads all pattern families and exposes
    them through a single interface.
    """

    def __init__(
        self,
    ):

        self.patterns = []

        self._load_patterns()

    # ---------------------------------------------------------
    # PRIVATE
    # ---------------------------------------------------------

    def _load_patterns(
        self,
    ) -> None:
        """
        Load every pattern family.
        """

        self.patterns.extend(
            AggregatePatterns.get_patterns()
        )

        self.patterns.extend(
            RankingPatterns.get_patterns()
        )

        self.patterns.extend(
            ComparisonPatterns.get_patterns()
        )

        self.patterns.extend(
            EvolutionPatterns.get_patterns()
        )

        self.patterns.extend(
            GeographicPatterns.get_patterns()
        )

        self.patterns.extend(
            StatisticalPatterns.get_patterns()
        )

    # ---------------------------------------------------------
    # PUBLIC
    # ---------------------------------------------------------

    def get_all_patterns(
        self,
    ) -> list[dict]:
        """
        Return every SQL pattern.
        """

        return self.patterns

    def get_patterns_by_category(
        self,
        category: str,
    ) -> list[dict]:
        """
        Return every pattern belonging
        to a given category.
        """

        return [

            pattern

            for pattern in self.patterns

            if pattern["category"].lower()
            == category.lower()

        ]