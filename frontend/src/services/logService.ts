import api from "../api/axios";

import type {

    LogDetails,

    LogSummary,

    LogsResponse,

    LogResponse,

} from "../types/log";


export interface ConversationLogsResponse {

    success: boolean;

    conversation_uuid: string;

    conversation_title: string;

    logs: LogSummary[];

}


// ======================================================
// ALL LOGS (optionnel)
// ======================================================

export async function getLogs(): Promise<LogSummary[]> {

    const response = await api.get<LogsResponse>(

        "/logs"

    );

    return response.data.logs;

}


// ======================================================
// ONE LOG
// ======================================================

export async function getLog(

    id: number

): Promise<LogDetails> {

    const response = await api.get<LogResponse>(

        `/logs/${id}`

    );

    return response.data.log;

}


// ======================================================
// LOGS OF ONE CONVERSATION
// ======================================================

export async function getConversationLogs(

    conversation_uuid: string

): Promise<ConversationLogsResponse> {

    const response = await api.get<ConversationLogsResponse>(

        `/conversations/${conversation_uuid}/logs`

    );

    return response.data;

}