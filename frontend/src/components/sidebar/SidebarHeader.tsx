import { useChatStore } from "../../store/chatStore";
import { useConversationStore } from "../../store/conversationStore";

const SidebarHeader = () => {

  const createNewConversation = useConversationStore(
    state => state.createNewConversation
  );

  const clearMessages = useChatStore(
    state => state.clearMessages
  );

  const handleNewChat = async () => {

    await createNewConversation();

    const activeConversation =
      useConversationStore.getState().activeConversation;

    if (activeConversation) {

      localStorage.setItem(

        "activeConversationUuid",

        activeConversation.conversation_uuid

      );

    }

    clearMessages();

  };

  return (

    <div className="p-4 border-b border-gray-800">

      <button

        onClick={handleNewChat}

        className="
          w-full
          rounded-lg
          bg-[#2f2f2f]
          hover:bg-[#3b3b3b]
          py-3
          transition
        "

      >

        + Nouveau chat

      </button>

    </div>

  );

};

export default SidebarHeader;