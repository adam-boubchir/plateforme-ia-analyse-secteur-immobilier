CREATE TABLE model_config (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    agent_name NVARCHAR(100) NOT NULL,

    provider NVARCHAR(50) NOT NULL,

    model_name NVARCHAR(100) NOT NULL,

    api_key_alias NVARCHAR(100) NULL,

    temperature DECIMAL(3,2) NOT NULL DEFAULT 0.00,

    max_tokens INT NOT NULL DEFAULT 1000,

    is_active BIT NOT NULL DEFAULT 1,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NULL,

    api_base_url NVARCHAR(500) NULL,

    deployment_name NVARCHAR(255) NULL,

    system_prompt NVARCHAR(MAX) NULL,

    timeout_seconds INT NOT NULL DEFAULT 60,

    top_p DECIMAL(3,2) NOT NULL DEFAULT 1.00,

    frequency_penalty DECIMAL(3,2) NOT NULL DEFAULT 0.00,

    presence_penalty DECIMAL(3,2) NOT NULL DEFAULT 0.00

);
CREATE INDEX IX_model_config_agent_name
ON model_config(agent_name);