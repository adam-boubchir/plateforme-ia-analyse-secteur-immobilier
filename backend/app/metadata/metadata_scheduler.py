from app.database.session import SessionLocal

from app.metadata.metadata_extractor import (
    MetadataExtractor
)

from app.metadata.metadata_loader import (
    MetadataLoader
)

from app.metadata.metadata_models import (
    MetadataLoadResult
)


class MetadataScheduler:

    def __init__(self):

        self.extractor = MetadataExtractor()

    def run(self) -> MetadataLoadResult:

        db = SessionLocal()

        try:

            loader = MetadataLoader(db)

            global_result = MetadataLoadResult()

            # ==========================
            # Extraction
            # ==========================

            tables = self.extractor.extract_tables()

            columns = self.extractor.extract_columns()

            relationships = (
                self.extractor.extract_relationships()
            )

            # ==========================
            # Chargement
            # ==========================

            return loader.load(
                tables=tables,
                columns=columns,
                relationships=relationships
            )

        finally:

            db.close()