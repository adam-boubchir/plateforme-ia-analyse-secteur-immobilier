import { create } from "zustand";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
}

interface ChatStore {
  conversations: Conversation[];
  activeConversationId: string | null;

  addConversation: () => void;
  setActiveConversation: (id: string) => void;
  addMessage: (role: "user" | "assistant", content: string) => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({

  conversations: [
    {
      id: crypto.randomUUID(),
      title: "Nouveau chat",
      messages: [
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Bonjour 👋, je suis votre assistant immobilier."
        }
      ]
    }
  ],

  activeConversationId: null,

  addConversation: () => {

    const id = crypto.randomUUID();

    const conversation: Conversation = {
      id,
      title: "Nouveau chat",
      messages: [
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Bonjour 👋, je suis votre assistant immobilier."
        }
      ]
    };

    set(state => ({
      conversations: [...state.conversations, conversation],
      activeConversationId: id
    }));
  },

  setActiveConversation: (id) => {

    set({
      activeConversationId: id
    });

  },

  addMessage: (role, content) => {

    const state = get();

    const activeId =
      state.activeConversationId ??
      state.conversations[0].id;

    const conversations = state.conversations.map(c => {

      if (c.id !== activeId)
        return c;

      return {

        ...c,

        messages: [

          ...c.messages,

          {
            id: crypto.randomUUID(),
            role,
            content
          }

        ]

      };

    });

    set({
      conversations
    });

  }

}));