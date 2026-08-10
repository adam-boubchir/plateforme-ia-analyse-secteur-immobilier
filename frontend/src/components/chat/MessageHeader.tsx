import {
    Bot,
    User,
    ShieldCheck,
    Clock,
    Cpu,
    Sparkles,
    Database,
} from "lucide-react";

type Props = {
    role: "user" | "assistant";
};

const MessageHeader = ({ role }: Props) => {

    const isUser = role === "user";

    const currentTime = new Date().toLocaleTimeString(
        "fr-FR",
        {
            hour: "2-digit",
            minute: "2-digit",
        },
    );

    return (

        <div
            className="
                flex
                items-center
                justify-between
                gap-6
            "
        >

            {/* LEFT */}

            <div className="flex items-center gap-5">

                <div
                    className={`
                        relative
                        flex
                        h-14
                        w-14
                        items-center
                        justify-center
                        rounded-2xl
                        shadow-xl
                        transition-all
                        duration-300
                        ${
                            isUser
                                ? `
                                    bg-gradient-to-br
                                    from-blue-600
                                    to-cyan-500
                                    shadow-blue-500/30
                                  `
                                : `
                                    bg-gradient-to-br
                                    from-emerald-500
                                    via-teal-500
                                    to-cyan-600
                                    shadow-emerald-500/30
                                  `
                        }
                    `}
                >

                    <div
                        className="
                            absolute
                            inset-0
                            rounded-2xl
                            bg-white/10
                            blur-xl
                        "
                    />

                    <div className="relative">

                        {
                            isUser
                                ? <User size={24} />
                                : <Bot size={24} />
                        }

                    </div>

                </div>

                <div>

                    <div
                        className="
                            flex
                            items-center
                            gap-3
                            flex-wrap
                        "
                    >

                        <h3
                            className="
                                text-lg
                                font-bold
                                tracking-tight
                                text-white
                            "
                        >

                            {
                                isUser
                                    ? "Vous"
                                    : "Plateforme Immobilier AI"
                            }

                        </h3>

                        {

                            !isUser && (

                                <>
                                    <Sparkles
                                        size={16}
                                        className="text-cyan-400"
                                    />

                                    <span
                                        className="
                                            rounded-full
                                            border
                                            border-cyan-500/20
                                            bg-cyan-500/10
                                            px-3
                                            py-1
                                            text-[11px]
                                            font-semibold
                                            uppercase
                                            tracking-wider
                                            text-cyan-300
                                        "
                                    >
                                        Analyse SQL
                                    </span>

                                </>

                            )

                        }

                    </div>

                    <div
                        className="
                            mt-2
                            flex
                            flex-wrap
                            items-center
                            gap-3
                            text-xs
                            text-slate-400
                        "
                    >

                        {

                            isUser

                                ? (

                                    <span>
                                        Utilisateur
                                    </span>

                                )

                                : (

                                    <>

                                        <span className="flex items-center gap-1">

                                            <ShieldCheck
                                                size={13}
                                                className="text-emerald-400"
                                            />

                                            Assistant IA

                                        </span>

                                        <span>•</span>

                                        <span>SQL Agent</span>

                                        <span>•</span>

                                        <span>Reporting Engine</span>

                                    </>

                                )

                        }

                    </div>

                </div>

            </div>

            {/* RIGHT */}

            <div
                className="
                    flex
                    items-center
                    gap-3
                    flex-wrap
                    justify-end
                "
            >

                {

                    !isUser && (

                        <div
                            className="
                                hidden
                                xl:flex
                                items-center
                                gap-2
                                rounded-full
                                border
                                border-blue-500/20
                                bg-blue-500/10
                                px-3
                                py-2
                                text-xs
                                font-medium
                                text-blue-300
                            "
                        >

                            <Cpu size={14} />

                            GPT-5 Nano

                        </div>

                    )

                }

                {

                    !isUser && (

                        <div
                            className="
                                hidden
                                xl:flex
                                items-center
                                gap-2
                                rounded-full
                                border
                                border-violet-500/20
                                bg-violet-500/10
                                px-3
                                py-2
                                text-xs
                                font-medium
                                text-violet-300
                            "
                        >

                            <Database size={14} />

                            Azure OpenAI

                        </div>

                    )

                }

                {

                    !isUser && (

                        <div
                            className="
                                flex
                                items-center
                                gap-2
                                rounded-full
                                border
                                border-emerald-500/20
                                bg-emerald-500/10
                                px-3
                                py-2
                                text-xs
                                font-medium
                                text-emerald-300
                            "
                        >

                            <span
                                className="
                                    h-2
                                    w-2
                                    rounded-full
                                    bg-emerald-400
                                    animate-pulse
                                "
                            />

                            IA Active

                        </div>

                    )

                }

                <div
                    className="
                        hidden
                        lg:flex
                        items-center
                        gap-2
                        rounded-full
                        border
                        border-white/10
                        bg-white/5
                        px-3
                        py-2
                        text-xs
                        text-slate-400
                    "
                >

                    <Clock size={13} />

                    {currentTime}

                </div>

            </div>

        </div>

    );

};

export default MessageHeader;