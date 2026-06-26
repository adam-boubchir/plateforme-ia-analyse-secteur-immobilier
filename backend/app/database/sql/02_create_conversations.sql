CREATE TABLE conversations (

    id BIGINT IDENTITY(1,1) PRIMARY KEY,

    conversation_id UNIQUEIDENTIFIER NOT NULL,

    request_id UNIQUEIDENTIFIER NOT NULL,

    user_id NVARCHAR(100) NULL,

    agent_name NVARCHAR(100) NOT NULL,

    user_message NVARCHAR(MAX) NOT NULL,

    assistant_response NVARCHAR(MAX) NULL,

    status NVARCHAR(20) NOT NULL,

    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()

);
CREATE INDEX IX_conversations_conversation_id
ON conversations(conversation_id);

CREATE INDEX IX_conversations_request_id
ON conversations(request_id);

CREATE INDEX IX_conversations_created_at
ON conversations(created_at);