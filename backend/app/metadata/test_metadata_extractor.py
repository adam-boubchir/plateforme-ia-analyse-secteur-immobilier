from app.metadata.metadata_extractor import (
    MetadataExtractor
)

extractor = MetadataExtractor()

result = extractor.run()

print(result)