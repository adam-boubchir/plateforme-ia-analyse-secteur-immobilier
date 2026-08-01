from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AuditMetadata",
    "DatabaseServer",
    "DatabaseStatistics",
    "Schema",
    "Table",
    "View",
    "Column",
    "PrimaryKey",
    "ForeignKey",
    "Index",
    "TableStatistics",
    "AuditReport",
]


class AuditMetadata(BaseModel):
    """Metadata about the audit execution."""

    model_config = ConfigDict(extra="forbid")

    generated_at: datetime
    duration_ms: int = 0
    success: bool = True

    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class DatabaseServer(BaseModel):
    """Information about the SQL Server instance."""

    model_config = ConfigDict(extra="forbid")

    server_name: str
    database_name: str
    sql_server_version: str

    compatibility_level: int | None = None
    collation: str | None = None


class DatabaseStatistics(BaseModel):
    """Global database statistics."""

    model_config = ConfigDict(extra="forbid")

    total_tables: int = 0
    total_views: int = 0
    total_columns: int = 0
    total_primary_keys: int = 0
    total_foreign_keys: int = 0
    total_indexes: int = 0
    total_rows: int = 0


class Schema(BaseModel):
    """Database schema."""

    model_config = ConfigDict(extra="forbid")

    name: str


class Table(BaseModel):
    """Database table."""

    model_config = ConfigDict(extra="forbid")

    schema_name: str
    name: str
    table_type: str = "BASE TABLE"
    row_count: int = 0


class View(BaseModel):
    """Database view."""

    model_config = ConfigDict(extra="forbid")

    schema_name: str
    name: str


class Column(BaseModel):
    """Database column."""

    model_config = ConfigDict(extra="forbid")

    schema_name: str
    table: str
    name: str

    data_type: str
    nullable: bool

    max_length: int | None = None
    default_value: str | None = None


class PrimaryKey(BaseModel):
    """Primary key."""

    model_config = ConfigDict(extra="forbid")

    schema_name: str
    table: str
    column: str


class ForeignKey(BaseModel):
    """Foreign key relationship."""

    model_config = ConfigDict(extra="forbid")

    constraint_name: str

    source_schema: str
    source_table: str
    source_column: str

    target_schema: str
    target_table: str
    target_column: str


class Index(BaseModel):
    """Database index."""

    model_config = ConfigDict(extra="forbid")

    table: str
    name: str
    index_type: str
    unique: bool


class TableStatistics(BaseModel):
    """Statistics for a database table."""

    model_config = ConfigDict(extra="forbid")

    schema_name: str
    table: str

    row_count: int
    size_mb: float = 0.0


class AuditReport(BaseModel):
    """Complete database audit report."""

    model_config = ConfigDict(extra="forbid")

    metadata: AuditMetadata
    server: DatabaseServer
    statistics: DatabaseStatistics

    schemas: list[Schema] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    views: list[View] = Field(default_factory=list)
    columns: list[Column] = Field(default_factory=list)
    primary_keys: list[PrimaryKey] = Field(default_factory=list)
    foreign_keys: list[ForeignKey] = Field(default_factory=list)
    indexes: list[Index] = Field(default_factory=list)
    table_statistics: list[TableStatistics] = Field(default_factory=list)