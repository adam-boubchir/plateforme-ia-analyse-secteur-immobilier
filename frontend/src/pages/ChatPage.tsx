import ChatHeader from "../components/chat/ChatHeader";
import ChatMessages from "../components/chat/ChatMessages";
import ChatInput from "../components/chat/ChatInput";

const ChatPage = () => {
  return (
    <main className="flex-1 flex flex-col h-screen">

      <ChatHeader />

      <ChatMessages />

      <ChatInput />

    </main>
  );
};

export default ChatPage;