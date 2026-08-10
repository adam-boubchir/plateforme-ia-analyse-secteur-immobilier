import { useEffect, useRef, useState } from "react";
import {
  MoreHorizontal,
  Pencil,
  Trash2,
  MessageSquare,
  FileText,
} from "lucide-react";

import type { Conversation } from "../../types/conversation";
import { useConversationStore } from "../../store/conversationStore";
import { useNavigate } from "react-router-dom";

type Props = {
  conversation: Conversation;
};

const ConversationItem = ({ conversation }: Props) => {
  const activeConversation = useConversationStore(
    (state) => state.activeConversation
  );

  const removeConversation = useConversationStore(
    (state) => state.removeConversation
  );

  const renameConversation = useConversationStore(
    (state) => state.renameConversation
  );

  const openedMenuConversationUuid = useConversationStore(
    (state) => state.openedMenuConversationUuid
  );

  const setOpenedMenu = useConversationStore(
    (state) => state.setOpenedMenu
  );

  const selectConversation = useConversationStore(
    (state) => state.selectConversation
  );

  const [isEditing, setIsEditing] = useState(false);

  const [title, setTitle] = useState(
    conversation.title ?? ""
  );

  const inputRef = useRef<HTMLInputElement>(null);

  const menuRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate();

  const menuOpen =
    openedMenuConversationUuid ===
    conversation.conversation_uuid;

  const isActive =
    activeConversation?.conversation_uuid ===
    conversation.conversation_uuid;

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [isEditing]);

  const handleClick = async () => {
    setOpenedMenu(null);

    await selectConversation(
      conversation.conversation_uuid
    );

    navigate("/chat");
  };

  const handleDelete = async (
    e: React.MouseEvent
  ) => {
    e.stopPropagation();

    if (
      !window.confirm(
        "Voulez-vous vraiment supprimer cette conversation ?"
      )
    ) {
      return;
    }

    await removeConversation(
      conversation.conversation_uuid
    );
  };

  const saveTitle = async () => {
    const newTitle = title.trim();

    setIsEditing(false);

    setOpenedMenu(null);

    if (
      newTitle === "" ||
      newTitle === conversation.title
    ) {
      setTitle(
        conversation.title ?? ""
      );

      return;
    }

    await renameConversation(
      conversation.conversation_uuid,
      newTitle
    );
  };

  useEffect(() => {
    const handleClickOutside = (
      event: MouseEvent
    ) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(
          event.target as Node
        )
      ) {
        setOpenedMenu(null);
      }
    };

    document.addEventListener(
      "click",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "click",
        handleClickOutside
      );
    };
  }, [setOpenedMenu]);

  return (
    <div
      ref={menuRef}
      className="relative group px-2 py-1"
    >
      {isEditing ? (
        <input
          ref={inputRef}
          value={title}
          onChange={(e) =>
            setTitle(e.target.value)
          }
          onBlur={saveTitle}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              saveTitle();
            }

            if (e.key === "Escape") {
              setTitle(
                conversation.title ?? ""
              );

              setIsEditing(false);

              setOpenedMenu(null);
            }
          }}
          className="
            w-full
            rounded-2xl
            border
            border-blue-500
            bg-[#202020]
            px-4
            py-3
            text-white
            outline-none
            focus:ring-2
            focus:ring-blue-500/40
          "
        />
      ) : (
        <button
          onClick={handleClick}
          className={`
            relative

            w-full

            flex
            items-center
            gap-3

            rounded-2xl

            px-4
            py-3.5
            pr-12

            transition-all
            duration-300

            border

            ${
              isActive
                ? `
                    border-blue-500/40

                    bg-gradient-to-r
                    from-blue-600/90
                    to-cyan-600/90

                    shadow-lg
                    shadow-blue-500/25
                  `
                : `
                    border-transparent

                    hover:border-slate-700
                    hover:bg-slate-800/60
                  `
            }
          `}
        >
          <div
            className={`
              flex
              h-9
              w-9
              items-center
              justify-center

              rounded-xl

              ${
                isActive
                  ? "bg-white/20"
                  : "bg-slate-700/40"
              }
            `}
          >
            <MessageSquare
              size={17}
              className={
                isActive
                  ? "text-white"
                  : "text-slate-300"
              }
            />
          </div>

          <div className="flex-1 min-w-0 text-left">
            <div className="truncate text-sm font-semibold">
              {conversation.title ??
                "Nouvelle conversation"}
            </div>

            <div className="mt-1 text-xs text-slate-400">
              Conversation IA
            </div>
          </div>

          {isActive && (
            <div
              className="
                rounded-full
                bg-white/15
                px-2
                py-1
                text-[10px]
                font-medium
              "
            >
              Active
            </div>
          )}
        </button>
      )}

      {!isEditing && (
        <button
          onClick={(e) => {
            e.stopPropagation();

            if (menuOpen) {
              setOpenedMenu(null);
            } else {
              setOpenedMenu(
                conversation.conversation_uuid
              );
            }
          }}
          className="
            absolute
            right-4
            top-1/2
            -translate-y-1/2

            rounded-xl

            p-2

            opacity-0

            group-hover:opacity-100

            hover:bg-white/10

            transition-all
          "
        >
          <MoreHorizontal
            size={18}
            className="text-slate-400"
          />
        </button>
      )}

      {menuOpen && (
        <div
          className="
            absolute
            right-2
            top-full
            mt-2

            z-50

            w-56

            overflow-hidden

            rounded-2xl

            border
            border-slate-700

            bg-[#1c1c1c]/95

            backdrop-blur-xl

            shadow-2xl
          "
        >
          <button
            onClick={() => {
              setTitle(
                conversation.title ?? ""
              );

              setIsEditing(true);
            }}
            className="
              flex
              items-center
              gap-3

              w-full

              px-4
              py-3

              transition-colors

              hover:bg-slate-700/40
            "
          >
            <Pencil size={17} />

            Renommer
          </button>

          <button
            onClick={(e) => {
              e.stopPropagation();

              setOpenedMenu(null);

              navigate(
                `/conversations/${conversation.conversation_uuid}/logs`
              );
            }}
            className="
              flex
              items-center
              gap-3

              w-full

              px-4
              py-3

              transition-colors

              hover:bg-slate-700/40
            "
          >
            <FileText size={17} />

            Execution Logs
          </button>

          <button
            onClick={handleDelete}
            className="
              flex
              items-center
              gap-3

              w-full

              px-4
              py-3

              text-red-400

              transition-colors

              hover:bg-red-500/10
            "
          >
            <Trash2 size={17} />

            Supprimer
          </button>
        </div>
      )}
    </div>
  );
};

export default ConversationItem;