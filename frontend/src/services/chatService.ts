import api from "../api/axios";

import type {
    ChatRequest,
    ChatResponse,
} from "../types/chat";

/**
 * Send a user question to the backend AI platform.
 *
 * Returns:
 * - AI answer
 * - Generated SQL
 * - SQL rows
 * - PDF path if available
 */
export async function sendMessage(
    request: ChatRequest,
): Promise<ChatResponse> {

    try {

        const response = await api.post<ChatResponse>(
            "/chat",
            request,
        );

        return response.data;

    } catch (error: unknown) {

        console.error(
            "Chat API error:",
            error,
        );

        if (
            typeof error === "object" &&
            error !== null &&
            "response" in error
        ) {

            const axiosError = error as {
                response?: {
                    data?: ChatResponse;
                };
            };

            if (axiosError.response?.data) {

                return axiosError.response.data;

            }

        }

        return {
            success: false,

            conversation_uuid: null,

            answer: "",

            sql: null,

            rows: [],

            pdf_path: null,

            error:
                "Impossible de communiquer avec le serveur.",
        };

    }
}