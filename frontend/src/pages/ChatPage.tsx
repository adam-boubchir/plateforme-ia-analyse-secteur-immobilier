import ChatHeader from "../components/chat/ChatHeader";
import ChatMessages from "../components/chat/ChatMessages";
import ChatInput from "../components/chat/ChatInput";

const ChatPage = () => {
  return (
    <main
      className="
        flex-1

        h-full

        flex
        flex-col

        overflow-hidden
      "
    >
      {/* Header fixe */}

      <div
        className="
          shrink-0
        "
      >
        <ChatHeader />
      </div>

      {/* Zone centrale */}

      <section
        className="
          flex-1

          flex
          justify-center

          overflow-hidden

          px-6
          py-4
        "
      >
        <div
          className="
            flex

            h-full
            w-full
            max-w-7xl

            flex-col

            overflow-hidden
          "
        >
          <ChatMessages />
        </div>
      </section>

      {/* Input fixe */}

      <div
        className="
          shrink-0
        "
      >
        <ChatInput />
      </div>
    </main>
  );
};

export default ChatPage;