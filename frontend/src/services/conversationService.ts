import api from "../api/axios";

import type {
    Conversation,
    ConversationDetails,
    CreateConversationRequest,
} from "../types/conversation";

export async function getConversations(): Promise<Conversation[]> {

    const response = await api.get("/conversations");

    return response.data;

}

export async function createConversation(

    data: CreateConversationRequest = {}

): Promise<Conversation> {

    const response = await api.post(

        "/conversations",

        data

    );

    return response.data;

}

export async function getConversation(

    conversation_uuid: string

): Promise<Conversation> {

    const response = await api.get(

        `/conversations/${conversation_uuid}`

    );

    return response.data;

}

export async function deleteConversation(

    conversation_uuid: string

): Promise<void> {

    await api.delete(

        `/conversations/${conversation_uuid}`

    );

}
export async function getConversationDetails(
    conversation_uuid: string
): Promise<ConversationDetails> {

    const response = await api.get(
        `/conversations/${conversation_uuid}`
    );

    return response.data;

}
export async function renameConversation(

    conversation_uuid: string,

    title: string

): Promise<Conversation> {

    const response = await api.patch(

        `/conversations/${conversation_uuid}`,

        {

            title,

        }

    );

    return response.data;

}