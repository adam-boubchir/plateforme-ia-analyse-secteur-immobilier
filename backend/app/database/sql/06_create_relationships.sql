CREATE TABLE relationships (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    source_table NVARCHAR(255) NOT NULL,

    source_column NVARCHAR(255) NOT NULL,

    target_table NVARCHAR(255) NOT NULL,

    target_column NVARCHAR(255) NOT NULL,

    relationship_type NVARCHAR(50) NULL,

    description NVARCHAR(MAX) NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NULL

);
CREATE INDEX IX_relationships_source_table
ON relationships(source_table);

CREATE INDEX IX_relationships_target_table
ON relationships(target_table);