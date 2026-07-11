import { useEffect, useRef, useState } from "react";
import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";

import type { Conversation } from "../../types/conversation";

import { useConversationStore } from "../../store/conversationStore";


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

  <div ref={menuRef} className="relative group mb-1">

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
            rounded-lg
            bg-[#2f2f2f]
            p-3
            outline-none
            border
            border-blue-500
          "

        />

      ) : (

        <button

          onClick={handleClick}

          className={`
            w-full
            text-left
            rounded-lg
            p-3
            pr-10
            truncate
            transition
            ${
              isActive
                ? "bg-blue-600"
                : "hover:bg-[#2f2f2f]"
            }
          `}

        >

          {

            conversation.title ??

            "Nouvelle conversation"

          }

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
            right-2
            top-1/2
            -translate-y-1/2
            opacity-0
            group-hover:opacity-100
            transition
          "

        >

          <MoreHorizontal size={18} />

        </button>

      )

    }

    {

      menuOpen && (

        <div
          className="
            absolute
            right-0
            mt-1
            w-44
            rounded-lg
            border
            border-gray-700
            bg-[#252525]
            shadow-xl
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
              gap-2
              w-full
              px-4
              py-2
              hover:bg-[#333]
            "

          >

            <Pencil size={16} />

            Renommer

          </button>

          <button

            onClick={handleDelete}

            className="
              flex
              items-center
              gap-2
              w-full
              px-4
              py-2
              text-red-400
              hover:bg-[#333]
            "

          >

            <Trash2 size={16} />

            Supprimer

          </button>

        </div>

      )

    }

  </div>

);
};

export default ConversationItem;