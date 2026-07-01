CREATE TABLE conversations (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    conversation_uuid UNIQUEIDENTIFIER NOT NULL UNIQUE,

    title NVARCHAR(255) NOT NULL,

    user_id NVARCHAR(100) NULL,

    status NVARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()

);

CREATE TABLE conversation_messages (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    conversation_id BIGINT NOT NULL,

    request_id UNIQUEIDENTIFIER NOT NULL,

    role NVARCHAR(20) NOT NULL,

    content NVARCHAR(MAX) NOT NULL,

    generated_sql NVARCHAR(MAX) NULL,

    execution_time_ms INT NULL,

    rows_returned INT NULL,

    status NVARCHAR(20) NOT NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT FK_conversation_messages_conversations
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE

);

CREATE UNIQUE INDEX IX_conversations_uuid
ON conversations(conversation_uuid);

CREATE INDEX IX_conversations_updated_at
ON conversations(updated_at);

CREATE INDEX IX_conversations_user
ON conversations(user_id);

CREATE INDEX IX_messages_conversation
ON conversation_messages(conversation_id);

CREATE INDEX IX_messages_request
ON conversation_messages(request_id);

CREATE INDEX IX_messages_created
ON conversation_messages(created_at);

CREATE INDEX IX_messages_role
ON conversation_messages(role);