CREATE TABLE column_metadata (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    table_id BIGINT NOT NULL,

    schema_name NVARCHAR(255) NOT NULL,

    table_name NVARCHAR(255) NOT NULL,

    column_name NVARCHAR(255) NOT NULL,

    business_name NVARCHAR(255) NULL,

    description NVARCHAR(MAX) NULL,

    data_type NVARCHAR(100) NOT NULL,

    max_length INT NULL,

    ordinal_position INT NULL,

    default_value NVARCHAR(MAX) NULL,

    is_nullable BIT NOT NULL,

    is_primary_key BIT NOT NULL DEFAULT 0,

    is_foreign_key BIT NOT NULL DEFAULT 0,

    sample_values NVARCHAR(MAX) NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NULL,

    CONSTRAINT FK_column_metadata_table
        FOREIGN KEY (table_id)
        REFERENCES table_metadata(id)

);

CREATE INDEX IX_column_metadata_table_id
ON column_metadata(table_id);

CREATE INDEX IX_column_metadata_schema_name
ON column_metadata(schema_name);

CREATE INDEX IX_column_metadata_table_name
ON column_metadata(table_name);

CREATE INDEX IX_column_metadata_column_name
ON column_metadata(column_name);