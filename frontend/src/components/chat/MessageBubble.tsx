type Props = {
  role: "user" | "assistant";
  content: string;
};

const MessageBubble = ({ role, content }: Props) => {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`
          max-w-3xl
          rounded-xl
          px-5
          py-3
          whitespace-pre-wrap
          ${
            isUser
              ? "bg-blue-600"
              : "bg-[#2f2f2f]"
          }
        `}
      >
        {content}
      </div>
    </div>
  );
};

export default MessageBubble;