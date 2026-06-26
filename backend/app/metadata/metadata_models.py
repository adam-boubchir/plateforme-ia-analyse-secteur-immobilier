from pydantic import BaseModel
from typing import Optional
from pydantic import Field
from __future__ import annotations

class TableMetadata(BaseModel):
    source_database: str
    schema_name_name: str
    table_name: str
    business_name: Optional[str] = None
    description: Optional[str] = None
    row_count: Optional[int] = None
    is_active: bool = True

class ColumnMetadata(BaseModel):
    table_name: str
    column_name: str
    business_name: Optional[str] = None
    description: Optional[str] = None
    data_type: str
    is_nullable: bool
    is_primary_key: bool = False
    is_foreign_key: bool = False
    sample_values: Optional[str] = None

class RelationshipMetadata(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    relationship_type: Optional[str] = None
    description: Optional[str] = None

class MetadataLoadResult(BaseModel):
    tables_processed: int = 0
    columns_processed: int = 0
    relationships_processed: int = 0
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    success: bool = True
    def merge(self, other: "MetadataLoadResult") -> None:

        self.tables_processed += other.tables_processed

        self.columns_processed += other.columns_processed

        self.relationships_processed += (
            other.relationships_processed
        )

        self.errors.extend(other.errors)

        self.warnings.extend(other.warnings)

        if not other.success:
            self.success = False

