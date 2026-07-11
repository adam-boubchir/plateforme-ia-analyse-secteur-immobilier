export interface Conversation {

    id: number;

    conversation_uuid: string;

    title: string | null;

    user_id: string | null;

    status: string;

    created_at: string;

    updated_at: string;

    last_message_at: string;

}

export interface CreateConversationRequest {

    title?: string;

    user_id?: string;

}

export interface ConversationMessage {

    role: "USER" | "ASSISTANT";

    content: string;

    generated_sql: string | null;

    rows: Record<string, unknown>[] | null;

    rows_returned: number | null;

    execution_time_ms: number | null;

    status: string;

    created_at: string;

}

export interface ConversationDetails extends Conversation {

    messages: ConversationMessage[];

}