export interface ChatRequest {

    question: string;

    conversation_uuid?: string | null;

}

export interface ChatResponse {
    success: boolean;
    conversation_uuid: string | null;
    answer: string;
    sql: string | null;
    rows: unknown[];
    error: string | null;
}