export interface LogSummary {

    id: number;

    conversation_id: number;

    question: string;

    status: string;

    execution_time_ms: number | null;

    created_at: string;

}

export interface LogDetails {

    id: number;

    conversation_id: number;

    message_id: number | null;

    question: string;

    selected_tables: string | null;

    business_knowledge: string | null;

    join_knowledge: string | null;

    forbidden_joins: string | null;

    semantic_context: string | null;

    sql_patterns: string | null;

    full_context: string | null;

    prompt: string | null;

    generated_sql: string | null;

    validated_sql: string | null;

    sql_result: string | null;

    formatted_answer: string | null;

    execution_time_ms: number | null;

    status: string;

    error_message: string | null;

    created_at: string;

}

export interface LogsResponse {

    success: boolean;

    logs: LogSummary[];

}

export interface LogResponse {

    success: boolean;

    log: LogDetails;

}