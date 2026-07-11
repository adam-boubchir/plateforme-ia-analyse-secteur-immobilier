import { useState } from "react";

import { sendMessage } from "../../services/chatService";

import { useChatStore } from "../../store/chatStore";

import { useConversationStore } from "../../store/conversationStore";

const ChatInput = () => {

  const [question, setQuestion] = useState("");

  const addMessage = useChatStore(
    (state) => state.addMessage
  );

  const setLoading = useChatStore(
    (state) => state.setLoading
  );

  const isLoading = useChatStore(
    (state) => state.isLoading
  );

  const activeConversation = useConversationStore(
    (state) => state.activeConversation
  );

  const setCurrentConversation = useConversationStore(
    (state) => state.setCurrentConversation
  );

  const loadConversations = useConversationStore(
    (state) => state.loadConversations
  );

  const handleSend = async () => {

    if (!question.trim() || isLoading)
      return;

    const userQuestion = question.trim();

    addMessage({

      role: "user",

      content: userQuestion

    });

    setQuestion("");

    setLoading(true);

    try {

      const response = await sendMessage({

        question: userQuestion,

        conversation_uuid:
          activeConversation?.conversation_uuid

      });

      addMessage({

        role: "assistant",

        content: response.answer,

        sql: response.sql,

        rows: response.rows

      });

      await loadConversations();

      if (response.conversation_uuid) {

        setCurrentConversation(
          response.conversation_uuid
        );

      }

    }

    catch (error) {

      console.error(error);

      addMessage({

        role: "assistant",

        content:
          "❌ Une erreur est survenue lors de la communication avec le serveur."

      });

    }

    finally {

      setLoading(false);

    }

  };

  return (

    <div className="border-t border-gray-800 p-6">

      <div className="flex gap-3">

        <input

          type="text"

          value={question}

          disabled={isLoading}

          onChange={(e) =>
            setQuestion(e.target.value)
          }

          onKeyDown={(e) => {

            if (e.key === "Enter") {

              handleSend();

            }

          }}

          placeholder="Posez votre question..."

          className="
            flex-1
            rounded-xl
            bg-[#2f2f2f]
            px-5
            py-4
            outline-none
            disabled:opacity-50
          "

        />

        <button

          onClick={handleSend}

          disabled={isLoading}

          className="
            bg-blue-600
            hover:bg-blue-700
            rounded-xl
            px-6
            font-medium
            transition-colors
            disabled:opacity-50
            disabled:cursor-not-allowed
          "

        >

          {isLoading ? "⏳" : "Envoyer"}

        </button>

      </div>

    </div>

  );

};

export default ChatInput;