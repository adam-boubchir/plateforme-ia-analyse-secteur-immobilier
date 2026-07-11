import api from "../api/axios";

import type {

  ChatRequest,

  ChatResponse,

} from "../types/chat";

export async function sendMessage(

  request: ChatRequest

): Promise<ChatResponse> {

  const response = await api.post(

    "/chat",

    request

  );

  return response.data;

}