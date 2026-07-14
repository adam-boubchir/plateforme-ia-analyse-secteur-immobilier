import ChatHeader from "../components/chat/ChatHeader";
import ChatMessages from "../components/chat/ChatMessages";
import ChatInput from "../components/chat/ChatInput";

const ChatPage = () => {

  return (

    <main
      className="
        flex
        flex-1
        flex-col
        h-screen
        bg-[#0f0f0f]
        overflow-hidden
      "
    >

      <ChatHeader />

      <div
        className="
          flex-1
          overflow-hidden
          flex
          justify-center
        "
      >

        <div
          className="
            w-full
            max-w-7xl
            flex
            flex-col
            overflow-hidden
          "
        >

          <ChatMessages />

        </div>

      </div>

      <ChatInput />

    </main>

  );

};

export default ChatPage;