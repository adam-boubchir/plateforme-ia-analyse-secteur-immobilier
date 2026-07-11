import { useChatStore } from "../../store/chatStore";
import MessageBubble from "./MessageBubble";

const ChatMessages = () => {

  const messages = useChatStore(
    (state) => state.messages
  );

  const isLoading = useChatStore(
    (state) => state.isLoading
  );

  return (

    <div className="flex-1 overflow-y-auto p-8 space-y-6">

      {

        messages.map(

          (message) => (

            <MessageBubble

              key={message.id}

              role={message.role}

              content={message.content}

              sql={message.sql}

              rows={message.rows}

            />

          )

        )

      }

      {

        isLoading && (

          <MessageBubble

            role="assistant"

            content="⏳ L'assistant réfléchit..."

          />

        )

      }

    </div>

  );

};

export default ChatMessages;