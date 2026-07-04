import { useState } from "react";
import { sendMessage } from "../../services/chatService";

const ChatInput = () => {

  const [question, setQuestion] = useState("");

  const handleSend = async () => {

    if (!question.trim()) return;

    try {

      const response = await sendMessage(question);

      console.log(response);

      setQuestion("");

    } catch (error) {

      console.error(error);

    }

  };

  return (
    <div className="border-t border-gray-800 p-6">

      <div className="flex gap-3">

        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          placeholder="Posez votre question..."
          className="
            flex-1
            rounded-xl
            bg-[#2f2f2f]
            px-5
            py-4
            outline-none
          "
        />

        <button
          onClick={handleSend}
          className="
            bg-blue-600
            hover:bg-blue-700
            rounded-xl
            px-6
          "
        >
          Envoyer
        </button>

      </div>

    </div>
  );
};

export default ChatInput;