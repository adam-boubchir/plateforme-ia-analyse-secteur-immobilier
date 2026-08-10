import { useEffect, useRef } from "react";

import { useChatStore } from "../../store/chatStore";
import MessageBubble from "./MessageBubble";

const ChatMessages = () => {
    const messages = useChatStore(
        (state) => state.messages,
    );

    const isLoading = useChatStore(
        (state) => state.isLoading,
    );

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages, isLoading]);

    return (
        <div
            className="
                flex-1

                overflow-y-auto
                overflow-x-hidden

                scroll-smooth

                px-6
                md:px-10
                lg:px-14

                py-8
            "
        >
            <div
                className="
                    mx-auto

                    flex
                    flex-col

                    w-full
                    max-w-6xl

                    gap-8

                    pb-10
                "
            >
                {messages.map((message) => (
                    <MessageBubble
                        key={message.id}
                        role={message.role}
                        content={message.content}
                        sql={message.sql}
                        rows={message.rows}
                        pdf_path={message.pdf_path}
                    />
                ))}

                {isLoading && (
                    <MessageBubble
                        role="assistant"
                        content="🤖 Analyse de votre demande..."
                    />
                )}

                <div
                    ref={bottomRef}
                    className="h-2"
                />
            </div>
        </div>
    );
};

export default ChatMessages;    