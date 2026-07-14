from app.database.session import (
    SessionLocalImmoAI,
    SessionLocalMinistry,
)

from app.services.metadata_service import (
    MetadataService,
)

from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)

from app.database.repositories.semantic_keyword_repository import (
    SemanticKeywordRepository,
)

from app.services.semantic_metadata.semantic_keyword_service import (
    SemanticKeywordService,
)

from app.services.semantic_metadata.semantic_type_detector import (
    SemanticTypeDetector,
)

from app.services.semantic_metadata.statistics_extractor import (
    StatisticsExtractor,
)

from app.services.semantic_metadata.example_value_extractor import (
    ExampleValueExtractor,
)

from app.services.semantic_metadata.metadata_profiler import (
    MetadataProfiler,
)


def main():

    immo_db = SessionLocalImmoAI()

    ministry_db = SessionLocalMinistry()

    try:

        metadata_service = MetadataService(
            immo_db
        )

        column_repository = ColumnMetadataRepository(
            immo_db
        )

        keyword_repository = SemanticKeywordRepository(
            immo_db
        )

        keyword_service = SemanticKeywordService(
            keyword_repository
        )

        semantic_detector = SemanticTypeDetector(
            keyword_service
        )

        statistics_extractor = StatisticsExtractor(
            ministry_db
        )

        example_extractor = ExampleValueExtractor(
            ministry_db
        )

        profiler = MetadataProfiler(

            metadata_service=metadata_service,

            semantic_detector=semantic_detector,

            statistics_extractor=statistics_extractor,

            example_extractor=example_extractor,

            column_repository=column_repository,

        )

        profiler.profile_database()

        print("\n========================================")
        print("Profiling terminé avec succès.")
        print("========================================")

    finally:

        immo_db.close()

        ministry_db.close()


if __name__ == "__main__":

    main()