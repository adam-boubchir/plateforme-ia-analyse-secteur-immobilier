import { create } from "zustand";
import { persist } from "zustand/middleware";

import type {
  Conversation,
} from "../types/conversation";

import {
  getConversations,
  createConversation,
  deleteConversation,
  renameConversation as renameConversationApi,
  getConversationDetails,
} from "../services/conversationService";

import { useChatStore } from "./chatStore";

console.log("getConversationDetails =", getConversationDetails);
interface ConversationStore {

  conversations: Conversation[];

  activeConversation: Conversation | null;

  isLoading: boolean;

  openedMenuConversationUuid: string | null;

  loadConversations: () => Promise<void>;

  createNewConversation: () => Promise<void>;

  removeConversation: (
    conversation_uuid: string
  ) => Promise<void>;

  renameConversation: (
    conversation_uuid: string,
    title: string
  ) => Promise<void>;

  setActiveConversation: (
    conversation: Conversation
  ) => void;

  setCurrentConversation: (
    conversation_uuid: string
  ) => void;

  selectConversation: (
    conversation_uuid: string
  ) => Promise<void>;

  setOpenedMenu: (
    conversation_uuid: string | null
  ) => void;

}

export const useConversationStore =
create<ConversationStore>()(

persist(

(set, get) => ({

  conversations: [],

  activeConversation: null,

  isLoading: false,

  openedMenuConversationUuid: null,

  loadConversations: async () => {

    set({
      isLoading: true,
    });

    try {

      const conversations =
        await getConversations();

      set({

        conversations,

        isLoading: false,

      });

    }

    catch (error) {

      console.error(error);

      set({

        isLoading: false,

      });

    }

  },

  createNewConversation: async () => {

    try {

      const conversation =
        await createConversation();

      set(state => ({

        conversations: [

          conversation,

          ...state.conversations,

        ],

        activeConversation: conversation,

      }));

    }

    catch (error) {

      console.error(error);

    }

  },

  removeConversation: async (

    conversation_uuid

  ) => {

    try {

      await deleteConversation(
        conversation_uuid
      );

      const state = get();

      const conversations =
        state.conversations.filter(

          c =>

            c.conversation_uuid !==

            conversation_uuid

        );

      let activeConversation =
        state.activeConversation;

      if (

        activeConversation?.conversation_uuid ===

        conversation_uuid

      ) {

        activeConversation =

          conversations.length > 0

            ? conversations[0]

            : null;

      }

      set({

        conversations,

        activeConversation,

        openedMenuConversationUuid: null,

      });

    }

    catch (error) {

      console.error(error);

    }

  },

  renameConversation: async (

    conversation_uuid,

    title

  ) => {

    try {

      const updatedConversation =
        await renameConversationApi(

          conversation_uuid,

          title

        );

      set(state => ({

        conversations:

          state.conversations.map(

            conversation =>

              conversation.conversation_uuid ===

              conversation_uuid

                ? updatedConversation

                : conversation

          ),

        activeConversation:

          state.activeConversation?.conversation_uuid ===

          conversation_uuid

            ? updatedConversation

            : state.activeConversation,

        openedMenuConversationUuid: null,

      }));

    }

    catch (error) {

      console.error(error);

    }

  },

  setActiveConversation: (

    conversation

  ) => {

    set({

      activeConversation: conversation,

    });

  },

  setCurrentConversation: (

    conversation_uuid

  ) => {

    const conversation =

      get().conversations.find(

        c =>

          c.conversation_uuid ===

          conversation_uuid

      );

    if (conversation) {

      set({

        activeConversation: conversation,

      });

    }

  },

  selectConversation: async (

  conversation_uuid

) => {

  const conversation = get()

    .conversations.find(

      c =>

        c.conversation_uuid ===

        conversation_uuid

    );

  if (!conversation) {

    return;

  }

  set({

    activeConversation: conversation,

  });

  try {

    const details =

      await getConversationDetails(

        conversation_uuid

      );

    useChatStore.getState().setMessages(

      details.messages.map(message => ({

        id: crypto.randomUUID(),

        role:
          message.role === "USER"
            ? "user"
            : "assistant",

        content: message.content,

        sql: message.generated_sql,

        rows: message.rows ?? undefined,

        pdf_path: message.pdf_path ?? null,

      }))

    );

  }

  catch (error) {

    console.error(error);

  }

},

  setOpenedMenu: (

    conversation_uuid

  ) => {

    set({

      openedMenuConversationUuid:

        conversation_uuid,

    });

  },

}),

{

  name: "conversation-store",

  partialize: (state) => ({

    activeConversation:

      state.activeConversation,

  }),

}

)

);