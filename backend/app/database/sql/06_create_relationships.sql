CREATE TABLE relationships (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    constraint_name NVARCHAR(255) NOT NULL,

    source_schema NVARCHAR(255) NOT NULL,

    source_table NVARCHAR(255) NOT NULL,

    source_column NVARCHAR(255) NOT NULL,

    target_schema NVARCHAR(255) NOT NULL,

    target_table NVARCHAR(255) NOT NULL,

    target_column NVARCHAR(255) NOT NULL,

    relationship_type NVARCHAR(50) NULL,

    description NVARCHAR(MAX) NULL,

    is_active BIT NOT NULL DEFAULT 1,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NULL

);

CREATE INDEX IX_relationships_constraint_name
ON relationships(constraint_name);

CREATE INDEX IX_relationships_source_table
ON relationships(source_table);

CREATE INDEX IX_relationships_target_table
ON relationships(target_table);