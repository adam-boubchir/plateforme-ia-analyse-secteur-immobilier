from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "TableMetadata",
    "ColumnMetadata",
    "RelationshipMetadata",
    "MetadataLoadResult",
]


class TableMetadata(BaseModel):
    """
    Metadata describing one database table.
    """

    model_config = ConfigDict(extra="forbid")

    source_database: str
    schema_name: str
    table_name: str
    business_name: str | None = None
    description: str | None = None
    row_count: int | None = None
    is_active: bool = True


class ColumnMetadata(BaseModel):
    """
    Metadata describing one database column.
    """

    model_config = ConfigDict(extra="forbid")

    table_name: str
    column_name: str
    business_name: str | None = None
    description: str | None = None
    data_type: str
    is_nullable: bool
    is_primary_key: bool = False
    is_foreign_key: bool = False
    sample_values: str | None = None


class RelationshipMetadata(BaseModel):
    """
    Metadata describing one foreign key relationship.
    """

    model_config = ConfigDict(extra="forbid")

    source_table: str
    source_column: str
    target_table: str
    target_column: str
    relationship_type: str | None = None
    description: str | None = None


class MetadataLoadResult(BaseModel):
    """
    Result of a metadata loading operation.
    """

    model_config = ConfigDict(extra="forbid")

    tables_processed: int = 0
    columns_processed: int = 0
    relationships_processed: int = 0

    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    success: bool = True

    def merge(
        self,
        other: MetadataLoadResult,
    ) -> None:
        """
        Merge another loading result into this one.
        """

        self.tables_processed += other.tables_processed
        self.columns_processed += other.columns_processed
        self.relationships_processed += (
            other.relationships_processed
        )

        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

        self.success = (
            self.success
            and other.success
        )