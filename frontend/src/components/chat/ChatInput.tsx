import { useState } from "react";
import { ArrowUp } from "lucide-react";

import { sendMessage } from "../../services/chatService";
import { useChatStore } from "../../store/chatStore";
import { useConversationStore } from "../../store/conversationStore";

const ChatInput = () => {

  const [question, setQuestion] = useState("");

  const addMessage = useChatStore(
    state => state.addMessage
  );

  const setLoading = useChatStore(
    state => state.setLoading
  );

  const isLoading = useChatStore(
    state => state.isLoading
  );

  const activeConversation = useConversationStore(
    state => state.activeConversation
  );

  const setCurrentConversation = useConversationStore(
    state => state.setCurrentConversation
  );

  const loadConversations = useConversationStore(
    state => state.loadConversations
  );

  const handleSend = async () => {

    if (!question.trim() || isLoading) {

      return;

    }

    const userQuestion = question.trim();

    addMessage({

      role: "user",

      content: userQuestion,

    });

    setQuestion("");

    setLoading(true);

    try {

      const response = await sendMessage({

        question: userQuestion,

        conversation_uuid:
          activeConversation?.conversation_uuid,

      });

      addMessage({

        role: "assistant",

        content: response.answer,

        sql: response.sql,

        rows: response.rows,

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
          "❌ Une erreur est survenue lors de la communication avec le serveur.",

      });

    }

    finally {

      setLoading(false);

    }

  };

  return (

    <div
      className="
        border-t
        border-white/10
        bg-[#0f0f0f]
        px-8
        py-6
      "
    >

      <div
        className="
          mx-auto
          max-w-5xl
        "
      >

        <div
          className="
            flex
            items-end
            gap-3
            rounded-3xl
            border
            border-white/10
            bg-[#1b1b1b]
            px-5
            py-4
            shadow-xl
            transition-all
            focus-within:border-blue-500
            focus-within:shadow-blue-500/20
          "
        >

          <textarea

            rows={1}

            value={question}

            disabled={isLoading}

            onChange={(e) =>
              setQuestion(e.target.value)
            }

            onKeyDown={(e) => {

              if (

                e.key === "Enter" &&

                !e.shiftKey

              ) {

                e.preventDefault();

                handleSend();

              }

            }}

            placeholder="Posez une question sur les données immobilières..."

            className="
              flex-1
              resize-none
              bg-transparent
              text-white
              placeholder:text-gray-500
              outline-none
              max-h-40
              leading-7
            "

          />

          <button

            onClick={handleSend}

            disabled={
              isLoading ||
              question.trim() === ""
            }

            className="
              h-11
              w-11
              rounded-full
              bg-blue-600
              hover:bg-blue-500
              disabled:bg-[#333]
              disabled:cursor-not-allowed
              flex
              items-center
              justify-center
              transition-all
              shadow-lg
              hover:scale-105
            "

          >

            {

              isLoading

                ? "⏳"

                : <ArrowUp size={18} />

            }

          </button>

        </div>

        <p
          className="
            mt-3
            text-center
            text-xs
            text-gray-500
          "
        >

          Habitat AI peut générer des réponses inexactes. Vérifiez les résultats importants.

        </p>

      </div>

    </div>

  );

};

export default ChatInput; 