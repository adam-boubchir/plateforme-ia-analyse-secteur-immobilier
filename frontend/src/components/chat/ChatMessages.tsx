import { useEffect, useRef } from "react";

import { useChatStore } from "../../store/chatStore";
import MessageBubble from "./MessageBubble";

const ChatMessages = () => {

  const messages = useChatStore(
    state => state.messages
  );

  const isLoading = useChatStore(
    state => state.isLoading
  );

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({

      behavior: "smooth",

    });

  }, [messages, isLoading]);

  return (

    <div
      className="
        flex-1
        overflow-y-auto
        overflow-x-hidden
        px-10
        py-10
      "
    >

      <div
        className="
          mx-auto
          w-full
          max-w-5xl
          space-y-16
          animate-[fadeIn_.25s_ease]
        "
      >

        {

          messages.map(message => (

            <MessageBubble

              key={message.id}

              role={message.role}

              content={message.content}

              sql={message.sql}

              rows={message.rows}

            />

          ))

        }

        {

          isLoading && (

            <MessageBubble

              role="assistant"

              content="⏳ L'assistant réfléchit..."

            />

          )

        }

        <div ref={bottomRef} />

      </div>

    </div>

  );

};

export default ChatMessages;