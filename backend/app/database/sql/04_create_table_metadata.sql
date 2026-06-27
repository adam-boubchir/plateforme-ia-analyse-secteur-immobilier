CREATE TABLE table_metadata (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    source_database NVARCHAR(255) NOT NULL,

    schema_name NVARCHAR(255) NOT NULL,

    table_name NVARCHAR(255) NOT NULL,

    table_type NVARCHAR(50) NOT NULL,

    business_name NVARCHAR(255) NULL,

    description NVARCHAR(MAX) NULL,

    row_count BIGINT NULL,

    is_fact_table BIT NOT NULL DEFAULT 0,

    is_active BIT NOT NULL DEFAULT 1,

    last_refresh DATETIME2 NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NULL

);

CREATE INDEX IX_table_metadata_source_database
ON table_metadata(source_database);

CREATE INDEX IX_table_metadata_schema_name
ON table_metadata(schema_name);

CREATE INDEX IX_table_metadata_table_name
ON table_metadata(table_name);

CREATE INDEX IX_table_metadata_table_type
ON table_metadata(table_type);

CREATE INDEX IX_table_metadata_is_active
ON table_metadata(is_active);