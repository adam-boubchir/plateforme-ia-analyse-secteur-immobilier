from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AuditMetadata(BaseModel):
    """
    Metadata about the audit execution.
    """

    generated_at: datetime
    duration_ms: int = 0
    success: bool = True

    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class DatabaseServer(BaseModel):
    """
    Information about the SQL Server instance.
    """

    server_name: str
    database_name: str
    sql_server_version: str

    compatibility_level: int | None = None
    collation: str | None = None


class DatabaseStatistics(BaseModel):
    """
    Global statistics of the database.
    """

    total_tables: int = 0
    total_views: int = 0
    total_columns: int = 0
    total_primary_keys: int = 0
    total_foreign_keys: int = 0
    total_indexes: int = 0
    total_rows: int = 0


class Schema(BaseModel):
    """
    Represents a database schema.
    """

    name: str


class Table(BaseModel):
    """
    Represents a database table.
    """

    schema_name: str
    name: str
    table_type: str = "BASE TABLE"
    row_count: int = 0


class View(BaseModel):
    """
    Represents a database view.
    """

    schema_name: str
    name: str


class Column(BaseModel):
    """
    Represents a database column.
    """

    schema_name: str
    table: str
    name: str

    data_type: str

    nullable: bool

    max_length: int | None = None
    default_value: str | None = None


class PrimaryKey(BaseModel):
    """
    Represents a primary key.
    """

    schema_name: str
    table: str
    column: str


class ForeignKey(BaseModel):
    """
    Represents a foreign key relationship.
    """

    constraint_name: str

    source_schema: str
    source_table: str
    source_column: str

    target_schema: str
    target_table: str
    target_column: str


class Index(BaseModel):
    """
    Represents a database index.
    """

    table: str
    name: str
    index_type: str
    unique: bool


class TableStatistics(BaseModel):
    """
    Statistics for one database table.
    """

    schema_name: str
    table: str

    row_count: int
    size_mb: float = 0.0


class AuditReport(BaseModel):
    """
    Complete database audit report.
    """

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