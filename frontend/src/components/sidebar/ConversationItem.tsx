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
    state => state.activeConversation
  );

  const removeConversation = useConversationStore(
    state => state.removeConversation
  );

  const renameConversation = useConversationStore(
    state => state.renameConversation
  );

  const openedMenuConversationUuid = useConversationStore(
    state => state.openedMenuConversationUuid
  );

  const setOpenedMenu = useConversationStore(
    state => state.setOpenedMenu
  );

  const selectConversation = useConversationStore(
    state => state.selectConversation
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

      {

        isEditing ? (

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
              bg-[#1d1d1d]
              px-4
              py-3
              outline-none
              focus:ring-2
              focus:ring-blue-500/40
            "

          />

        ) : (

          <button

            onClick={handleClick}

            className={`
              w-full
              flex
              items-center
              gap-3
              rounded-2xl
              px-4
              py-3
              pr-12
              transition-all
              duration-200
              border
              ${
                isActive
                  ? `
                    bg-gradient-to-r
                    from-blue-600
                    to-cyan-600
                    border-blue-500
                    shadow-xl
                    shadow-blue-600/20
                  `
                  : `
                    border-transparent
                    hover:bg-[#202020]
                  `
              }
            `}

          >

            <MessageSquare
              size={18}
              className={
                isActive
                  ? "text-white"
                  : "text-gray-400"
              }
            />

            <div className="truncate font-medium flex-1">

              {

                conversation.title ??

                "Nouvelle conversation"

              }

            </div>

          </button>

        )

      }

      {

        !isEditing && (

          <button

            onClick={(e) => {

              e.stopPropagation();

              if (menuOpen) {

                setOpenedMenu(null);

              }

              else {

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
              rounded-lg
              p-1.5
              opacity-0
              group-hover:opacity-100
              hover:bg-white/10
              transition-all
            "

          >

            <MoreHorizontal
              size={18}
              className="text-gray-400"
            />

          </button>

        )

      }

      {

        menuOpen && (

          <div
            className="
              absolute
              right-2
              top-full
              mt-2
              w-52
              rounded-2xl
              overflow-hidden
              border
              border-white/10
              bg-[#181818]
              shadow-2xl
              z-50
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
                hover:bg-[#242424]
              "

            >

              <Pencil size={17}/>

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
        hover:bg-[#242424]
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
                hover:bg-red-500/10
              "

            >

              <Trash2 size={17}/>

              Supprimer

            </button>

          </div>

        )

      }

    </div>

  );

};

export default ConversationItem;