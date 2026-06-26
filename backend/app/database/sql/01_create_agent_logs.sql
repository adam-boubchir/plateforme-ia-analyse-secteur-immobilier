CREATE TABLE agent_logs (
    
    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    request_id UNIQUEIDENTIFIER NOT NULL,

    timestamp_utc DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    agent_name NVARCHAR(100) NOT NULL,

    model_name NVARCHAR(100) NULL,

    user_id NVARCHAR(100) NULL,

    user_question NVARCHAR(MAX) NULL,

    generated_sql NVARCHAR(MAX) NULL,

    execution_time_ms INT NULL,

    rows_returned INT NULL,

    status NVARCHAR(20) NOT NULL,

    error_message NVARCHAR(MAX) NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()

);
CREATE INDEX IX_agent_logs_request_id
ON agent_logs(request_id);

CREATE INDEX IX_agent_logs_timestamp
ON agent_logs(timestamp_utc);

CREATE INDEX IX_agent_logs_agent_name
ON agent_logs(agent_name);

CREATE INDEX IX_agent_logs_status
ON agent_logs(status);