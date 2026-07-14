from app.services.metadata_service import MetadataService

from app.services.semantic_metadata.semantic_type_detector import (
    SemanticTypeDetector,
)

from app.services.semantic_metadata.statistics_extractor import (
    StatisticsExtractor,
)

from app.services.semantic_metadata.example_value_extractor import (
    ExampleValueExtractor,
)

from app.database.repositories.column_metadata_repository import (
    ColumnMetadataRepository,
)


class MetadataProfiler:
    """
    Build semantic metadata for every column stored in column_metadata.
    """

    def __init__(
        self,
        metadata_service: MetadataService,
        semantic_detector: SemanticTypeDetector,
        statistics_extractor: StatisticsExtractor,
        example_extractor: ExampleValueExtractor,
        column_repository: ColumnMetadataRepository,
    ):

        self.metadata_service = metadata_service

        self.semantic_detector = semantic_detector

        self.statistics_extractor = statistics_extractor

        self.example_extractor = example_extractor

        self.column_repository = column_repository

    def profile_database(
        self,
    ) -> None:
        """
        Profile every table.
        """

        tables = self.metadata_service.get_tables()

        for table in tables:

            print(f"\nProfiling table : {table.table_name}")

            columns = self.metadata_service.get_columns(
                table.table_name
            )

            for column in columns:

                self.profile_column(column)

    def profile_column(
        self,
        column,
    ) -> None:
        """
        Profile one column.
        """

        print(
            f"   -> {column.column_name}"
        )

        semantic_type = self.semantic_detector.detect(
            column.column_name
        )

        statistics = (
            self.statistics_extractor.extract(
                table_name=column.table_name,
                column_name=column.column_name,
                data_type=column.data_type,
            )
        )

        example_values = (
            self.example_extractor.extract(
                table_name=column.table_name,
                column_name=column.column_name,
                data_type=column.data_type,
            )
        )

        self.column_repository.update_profile(
            column_id=column.id,
            semantic_type=semantic_type,
            example_values=example_values,
            min_value=statistics["min_value"],
            max_value=statistics["max_value"],
            distinct_count=statistics["distinct_count"],
        )