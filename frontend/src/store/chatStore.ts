import { create } from "zustand";

export interface Message {

  id: string;

  role: "user" | "assistant";

  content: string;

  sql?: string | null;

  rows?: unknown[];

}

interface ChatStore {

  messages: Message[];

  isLoading: boolean;

  setMessages: (
    messages: Message[]
  ) => void;

  addMessage: (
    message: Omit<Message, "id">
  ) => void;

  clearMessages: () => void;

  setLoading: (
    loading: boolean
  ) => void;

}

export const useChatStore = create<ChatStore>((set) => ({

  messages: [

    {

      id: crypto.randomUUID(),

      role: "assistant",

      content:
        "Bonjour 👋, je suis votre assistant immobilier."

    }

  ],

  isLoading: false,

  setMessages: (messages) => {

    set({

      messages

    });

  },

  addMessage: (message) => {

    set(state => ({

      messages: [

        ...state.messages,

        {

          id: crypto.randomUUID(),

          ...message

        }

      ]

    }));

  },

  clearMessages: () => {

    set({

        messages: [

            {

                id: crypto.randomUUID(),

                role: "assistant",

                content:
                    "Bonjour 👋, je suis votre assistant immobilier."

            }

        ]

    });

},

  setLoading: (loading) => {

    set({

      isLoading: loading

    });

  }

}));