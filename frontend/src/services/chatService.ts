import api from "../api/axios";
import type { ChatResponse } from "../types/chat";

export async function sendMessage(question: string): Promise<ChatResponse> {
  const response = await api.post("/chat", {
    question,
  });

  return response.data;
}