from __future__ import annotations

from app.database.session import SessionLocal
from app.metadata.metadata_extractor import MetadataExtractor
from app.metadata.metadata_loader import MetadataLoader
from app.metadata.metadata_models import MetadataLoadResult

__all__ = ["MetadataScheduler"]


class MetadataScheduler:
    """
    Orchestrates metadata extraction and loading.
    """

    def __init__(self) -> None:
        self.extractor = MetadataExtractor()

    def run(self) -> MetadataLoadResult:
        """
        Execute the complete metadata synchronization pipeline.
        """

        db = SessionLocal()

        try:
            loader = MetadataLoader(db)

            tables = self.extractor.extract_tables()

            columns = self.extractor.extract_columns()

            relationships = (
                self.extractor.extract_relationships()
            )

            return loader.load(
                tables=tables,
                columns=columns,
                relationships=relationships,
            )

        finally:
            db.close()