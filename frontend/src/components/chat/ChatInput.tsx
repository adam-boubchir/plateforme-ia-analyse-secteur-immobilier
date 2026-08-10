import { useState } from "react";
import { ArrowUp } from "lucide-react";

import { sendMessage } from "../../services/chatService";
import { useChatStore } from "../../store/chatStore";
import { useConversationStore } from "../../store/conversationStore";

const ChatInput = () => {

    const [question, setQuestion] = useState("");

    const addMessage = useChatStore(
        state => state.addMessage
    );

    const setLoading = useChatStore(
        state => state.setLoading
    );

    const isLoading = useChatStore(
        state => state.isLoading
    );

    const activeConversation = useConversationStore(
        state => state.activeConversation
    );

    const setCurrentConversation = useConversationStore(
        state => state.setCurrentConversation
    );

    const loadConversations = useConversationStore(
        state => state.loadConversations
    );

    const handleSend = async () => {

        if (!question.trim() || isLoading) {
            return;
        }

        const userQuestion = question.trim();

        addMessage({
            role: "user",
            content: userQuestion,
        });

        setQuestion("");

        setLoading(true);

        try {

            const response = await sendMessage({

                question: userQuestion,

                conversation_uuid:
                    activeConversation?.conversation_uuid,

            });

            addMessage({

                role: "assistant",

                content: response.answer,

                sql: response.sql,

                rows: response.rows,

                pdf_path: response.pdf_path,

            });
            await loadConversations();

            if (response.conversation_uuid) {

                setCurrentConversation(
                    response.conversation_uuid
                );

            }

        }

        catch (error) {

            console.error(error);

            addMessage({

                role: "assistant",

                content:
                    "❌ Une erreur est survenue lors de la communication avec le serveur.",

            });

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div
            className="
                shrink-0

                border-t
                border-white/10

                bg-[#0f172a]/80
                backdrop-blur-xl

                px-6
                py-5
            "
        >

            <div
                className="
                    mx-auto
                    w-full
                    max-w-6xl
                "
            >

                <div
                    className="
                        flex
                        items-end
                        gap-4

                        rounded-[30px]

                        border
                        border-slate-700/70

                        bg-[#1b1b1b]

                        px-6
                        py-5

                        shadow-2xl

                        transition-all
                        duration-300

                        focus-within:border-blue-500
                        focus-within:shadow-blue-500/20
                    "
                >

                    <textarea

                        rows={1}

                        value={question}

                        disabled={isLoading}

                        onChange={(e) =>
                            setQuestion(e.target.value)
                        }

                        onKeyDown={(e) => {

                            if (

                                e.key === "Enter" &&

                                !e.shiftKey

                            ) {

                                e.preventDefault();

                                handleSend();

                            }

                        }}

                        placeholder="Posez une question sur les données immobilières..."

                        className="
                            flex-1

                            resize-none

                            bg-transparent

                            text-[15px]
                            leading-7

                            text-white

                            placeholder:text-slate-500

                            outline-none

                            max-h-52
                        "

                    />

                    <button

                        onClick={handleSend}

                        disabled={
                            isLoading ||
                            question.trim() === ""
                        }

                        className="
                            flex

                            h-12
                            w-12

                            items-center
                            justify-center

                            rounded-2xl

                            bg-gradient-to-br
                            from-blue-600
                            to-cyan-500

                            text-white

                            shadow-xl

                            transition-all
                            duration-300

                            hover:scale-105
                            hover:shadow-blue-500/40

                            disabled:opacity-40
                            disabled:cursor-not-allowed
                            disabled:hover:scale-100
                        "

                    >

                        {

                            isLoading

                                ? <span className="animate-pulse">⏳</span>

                                : <ArrowUp size={20}/>

                        }

                    </button>

                </div>

                <div
                    className="
                        mt-3

                        flex
                        items-center
                        justify-between

                        px-2

                        text-xs

                        text-slate-500
                    "
                >

                    <span>

                        Entrée pour envoyer • Shift + Entrée pour une nouvelle ligne

                    </span>

                    <span>

                        Plateforme IA • Ministère de l'Habitat

                    </span>

                </div>

            </div>

        </div>

    );

};

export default ChatInput;