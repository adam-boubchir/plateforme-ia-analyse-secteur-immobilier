import { useEffect, useMemo, useState } from "react";
import {
    CalendarDays,
    MessageSquareText,
} from "lucide-react";

import ConversationItem from "./ConversationItem";
import SearchConversation from "./SearchConversation";

import { useConversationStore } from "../../store/conversationStore";

const ConversationList = () => {

    const conversations = useConversationStore(
        (state) => state.conversations,
    );

    const loadConversations = useConversationStore(
        (state) => state.loadConversations,
    );

    const [search, setSearch] = useState("");

    useEffect(() => {

        loadConversations();

    }, []);

    const filteredConversations = useMemo(() => {

        return conversations.filter((conversation) =>
            (conversation.title ?? "")
                .toLowerCase()
                .includes(search.toLowerCase()),
        );

    }, [conversations, search]);

    return (

        <div className="flex flex-col h-full">

            <SearchConversation
                value={search}
                onChange={setSearch}
            />

            {/* HEADER */}

            <div
                className="
                    sticky
                    top-0
                    z-10

                    border-b
                    border-slate-700/40

                    bg-[#171717]/95
                    backdrop-blur-xl

                    px-5
                    py-4
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-between
                    "
                >

                    <div className="flex items-center gap-2">

                        <CalendarDays
                            size={15}
                            className="text-cyan-400"
                        />

                        <span
                            className="
                                text-xs
                                font-semibold
                                uppercase
                                tracking-[0.20em]
                                text-slate-400
                            "
                        >

                            Conversations

                        </span>

                    </div>

                    <div
                        className="
                            rounded-full

                            bg-cyan-500/10

                            border
                            border-cyan-500/20

                            px-3
                            py-1

                            text-xs
                            font-medium

                            text-cyan-300
                        "
                    >

                        {filteredConversations.length}

                    </div>

                </div>

            </div>

            {/* LIST */}

            <div
                className="
                    flex-1

                    overflow-y-auto

                    px-3
                    py-4

                    space-y-2
                "
            >

                {

                    filteredConversations.length === 0 ? (

                        <div
                            className="
                                mt-12

                                flex
                                flex-col
                                items-center
                                justify-center

                                rounded-3xl

                                border
                                border-dashed
                                border-slate-700

                                bg-slate-800/20

                                px-6
                                py-10

                                text-center
                            "
                        >

                            <div
                                className="
                                    flex
                                    h-14
                                    w-14
                                    items-center
                                    justify-center

                                    rounded-2xl

                                    bg-cyan-500/10
                                "
                            >

                                <MessageSquareText
                                    size={28}
                                    className="text-cyan-400"
                                />

                            </div>

                            <h3
                                className="
                                    mt-5

                                    text-base
                                    font-semibold
                                "
                            >

                                Aucune conversation

                            </h3>

                            <p
                                className="
                                    mt-2

                                    text-sm

                                    leading-6

                                    text-slate-500
                                "
                            >

                                Lancez une nouvelle analyse afin de créer votre première conversation.

                            </p>

                        </div>

                    ) : (

                        filteredConversations.map((conversation) => (

                            <ConversationItem
                                key={conversation.conversation_uuid}
                                conversation={conversation}
                            />

                        ))

                    )

                }

            </div>

        </div>

    );

};

export default ConversationList;