import {
  MessageSquarePlus,
  Building2,
  Sparkles,
} from "lucide-react";

import { useChatStore } from "../../store/chatStore";
import { useConversationStore } from "../../store/conversationStore";

const SidebarHeader = () => {

  const createNewConversation =
    useConversationStore(
      state => state.createNewConversation
    );

  const clearMessages =
    useChatStore(
      state => state.clearMessages
    );

  const handleNewChat = async () => {

    await createNewConversation();

    clearMessages();

  };

  return (

    <div className="px-6 pt-7 pb-6 border-b border-white/10">

      <div className="flex items-center gap-4 mb-7">

        <div
          className="
            h-14
            w-14
            rounded-2xl
            bg-gradient-to-br
            from-blue-600
            via-cyan-500
            to-blue-700
            flex
            items-center
            justify-center
            shadow-xl
            shadow-blue-600/30
          "
        >

          <Building2 size={28}/>

        </div>

        <div>

          <div className="flex items-center gap-2">

            <h1 className="font-bold text-xl">

              Immobilier AI

            </h1>

            <Sparkles
              size={16}
              className="text-cyan-400"
            />

          </div>

          <p className="text-xs text-gray-400 mt-1">

            Assistant immobilier intelligent

          </p>

        </div>

      </div>

      <button

        onClick={handleNewChat}

        className="
          w-full
          rounded-2xl
          bg-gradient-to-r
          from-blue-600
          to-cyan-600
          hover:brightness-110
          transition-all
          duration-200
          py-3.5
          flex
          items-center
          justify-center
          gap-3
          font-medium
          shadow-xl
          shadow-blue-600/20
        "

      >

        <MessageSquarePlus size={20}/>

        Nouvelle conversation

      </button>

    </div>

  );

};

export default SidebarHeader;