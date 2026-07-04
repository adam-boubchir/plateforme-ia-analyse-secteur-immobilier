import MessageBubble from "./MessageBubble";

const ChatMessages = () => {
  return (
    <div className="flex-1 overflow-y-auto p-8 space-y-6">

      <MessageBubble
        role="assistant"
        content="Bonjour 👋, je suis votre assistant immobilier."
      />

      <MessageBubble
        role="user"
        content="Combien existe-t-il de communes ?"
      />

      <MessageBubble
        role="assistant"
        content="Je peux répondre à cette question dès que je serai connecté au backend."
      />

    </div>
  );
};

export default ChatMessages;