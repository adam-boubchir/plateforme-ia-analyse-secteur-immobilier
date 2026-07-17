import { useEffect } from "react";

import {
    useNavigate,
    useParams,
} from "react-router-dom";

import { useConversationStore } from "../../store/conversationStore";

import { useLogStore } from "../../store/logStore";

const ConversationLogsPage = () => {

    const navigate = useNavigate();

    const { conversation_uuid } = useParams();

    const activeConversation = useConversationStore(
        state => state.activeConversation
    );

    const {

        logs,

        loading,

        error,

        loadConversationLogs,

    } = useLogStore();

    useEffect(() => {

        if (!conversation_uuid) {

            return;

        }

        loadConversationLogs(
            conversation_uuid
        );

    }, [

        conversation_uuid,

        loadConversationLogs,

    ]);

    if (loading) {

        return (

            <div className="flex h-full items-center justify-center">

                Chargement des logs...

            </div>

        );

    }

    if (error) {

        return (

            <div className="flex h-full items-center justify-center text-red-500">

                {error}

            </div>

        );

    }

    return (

        <div className="h-full overflow-auto p-8">

            <button

                onClick={() => navigate(-1)}

                className="
                    mb-6
                    rounded-lg
                    bg-gray-700
                    px-4
                    py-2
                    hover:bg-gray-600
                "

            >

                ← Retour

            </button>

            <h1 className="text-3xl font-bold">

                Execution Logs

            </h1>

            <p className="mt-2 text-gray-400">

                {

                    activeConversation?.title ??

                    "Conversation"

                }

            </p>

            {

                logs.length === 0 && (

                    <div
                        className="
                            mt-10
                            rounded-xl
                            border
                            border-white/10
                            bg-[#171717]
                            p-8
                            text-center
                            text-gray-400
                        "
                    >

                        Aucun log disponible pour cette conversation.

                    </div>

                )

            }

            <div className="mt-8 space-y-4">

                {

                    logs.map(log => (

                        <div

                            key={log.id}

                            onClick={() =>

                                navigate(

                                    `/logs/${log.id}`

                                )

                            }

                            className="
                                cursor-pointer
                                rounded-xl
                                border
                                border-white/10
                                bg-[#171717]
                                p-5
                                transition-all
                                hover:border-blue-500
                                hover:bg-[#202020]
                            "

                        >

                            <div className="flex items-center justify-between">

                                <h2 className="text-lg font-semibold">

                                    {log.question}

                                </h2>

                                <span

                                    className={

                                        log.status === "SUCCESS"

                                            ? "rounded-full bg-green-500/20 px-3 py-1 text-sm text-green-400"

                                            : "rounded-full bg-red-500/20 px-3 py-1 text-sm text-red-400"

                                    }

                                >

                                    {log.status}

                                </span>

                            </div>

                            <div className="mt-4 flex gap-8 text-sm text-gray-400">

                                <span>

                                    ⏱ {log.execution_time_ms} ms

                                </span>

                                <span>

                                    {

                                        new Date(

                                            log.created_at

                                        ).toLocaleString()

                                    }

                                </span>

                            </div>

                        </div>

                    ))

                }

            </div>

        </div>

    );

};

export default ConversationLogsPage;