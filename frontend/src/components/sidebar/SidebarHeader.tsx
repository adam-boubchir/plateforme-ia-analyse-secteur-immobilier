import {
  Building2,
  MessageSquarePlus,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { useChatStore } from "../../store/chatStore";
import { useConversationStore } from "../../store/conversationStore";

const SidebarHeader = () => {
  const createNewConversation =
    useConversationStore(
      (state) => state.createNewConversation
    );

  const clearMessages =
    useChatStore(
      (state) => state.clearMessages
    );

  const handleNewChat = async () => {
    await createNewConversation();
    clearMessages();
  };

  return (
    <div
      className="
        px-6
        pt-7
        pb-6
        border-b
        border-white/10
      "
    >
      {/* Logo */}

      <div className="flex items-center gap-4 mb-7">

        <div
          className="
            relative
            flex
            h-16
            w-16
            items-center
            justify-center
            rounded-3xl

            bg-gradient-to-br
            from-blue-600
            via-cyan-500
            to-blue-700

            shadow-2xl
            shadow-blue-600/30
          "
        >
          <Building2 size={30} />

          <div
            className="
              absolute
              -right-1
              -top-1
              flex
              h-6
              w-6
              items-center
              justify-center
              rounded-full
              bg-emerald-500
              ring-4
              ring-[#171717]
            "
          >
            <Sparkles size={12} />
          </div>

        </div>

        <div className="flex-1">

          <div className="flex items-center gap-2">

            <h1
              className="
                text-xl
                font-bold
                tracking-wide
              "
            >
              Immobilier AI
            </h1>

          </div>

          <p
            className="
              mt-1
              text-xs
              text-slate-400
            "
          >
            Plateforme IA d'analyse immobilière
          </p>

          <div
            className="
              mt-2
              inline-flex
              items-center
              gap-2

              rounded-full
              border
              border-emerald-500/20

              bg-emerald-500/10

              px-3
              py-1

              text-[11px]
              font-medium
              text-emerald-300
            "
          >
            <ShieldCheck size={12} />

            IA connectée
          </div>

        </div>

      </div>

      {/* Bouton */}

      <button
        onClick={handleNewChat}
        className="
          group

          flex
          w-full
          items-center
          justify-center
          gap-3

          rounded-2xl

          bg-gradient-to-r
          from-blue-600
          to-cyan-600

          py-3.5

          font-medium

          shadow-xl
          shadow-blue-600/20

          transition-all
          duration-300

          hover:scale-[1.02]
          hover:shadow-blue-500/40
        "
      >

        <MessageSquarePlus
          size={20}
          className="
            transition-transform
            group-hover:rotate-90
          "
        />

        Nouvelle conversation

      </button>
    </div>
  );
};

export default SidebarHeader;