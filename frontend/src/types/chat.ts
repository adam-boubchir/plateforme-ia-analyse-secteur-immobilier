export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
}

export interface ChatRequest {
    question: string;
}

export interface ChatResponse {
    success: boolean;
    conversation_uuid: string | null;
    answer: string;
    sql: string | null;
    rows: unknown[];
    error: string | null;
}