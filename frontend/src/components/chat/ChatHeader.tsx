import {
    Building2,
    Sparkles,
    Database,
    ShieldCheck,
    Clock3,
    Cpu,
    Activity,
} from "lucide-react";

const ChatHeader = () => {

    const currentTime = new Date().toLocaleTimeString(
        "fr-FR",
        {
            hour: "2-digit",
            minute: "2-digit",
        },
    );

    return (

        <header
            className="
                sticky
                top-0
                z-40

                shrink-0

                border-b
                border-slate-700/40

                bg-[#0f172a]/85
                backdrop-blur-2xl

                px-8
                lg:px-10

                py-5

                flex
                items-center
                justify-between
            "
        >

            {/* ================================================= */}
            {/* LEFT */}
            {/* ================================================= */}

            <div className="flex items-center gap-5">

                <div
                    className="
                        relative

                        flex
                        h-16
                        w-16
                        items-center
                        justify-center

                        rounded-3xl

                        bg-gradient-to-br
                        from-blue-600
                        via-cyan-500
                        to-blue-700

                        shadow-xl
                        shadow-blue-600/30
                    "
                >

                    <div
                        className="
                            absolute
                            inset-0

                            rounded-3xl

                            bg-white/10

                            blur-xl
                        "
                    />

                    <Building2
                        size={30}
                        className="relative"
                    />

                </div>

                <div>

                    <div className="flex items-center gap-3">

                        <h1
                            className="
                                text-3xl
                                font-bold
                                tracking-tight
                                text-white
                            "
                        >

                            Plateforme Immobilier AI

                        </h1>

                        <Sparkles
                            size={18}
                            className="
                                text-cyan-400
                            "
                        />

                    </div>

                    <p
                        className="
                            mt-1

                            hidden
                            md:block

                            text-sm

                            text-slate-400
                        "
                    >

                        Plateforme intelligente d'analyse et de décision du secteur immobilier

                    </p>

                </div>

            </div>

            {/* ================================================= */}
            {/* RIGHT */}
            {/* ================================================= */}

            <div
                className="
                    flex
                    items-center
                    gap-3
                "
            >

                {/* GPT */}

                <div
                    className="
                        hidden
                        2xl:flex

                        items-center
                        gap-2

                        rounded-full

                        border
                        border-blue-500/20

                        bg-blue-500/10

                        px-4
                        py-2
                    "
                >

                    <Cpu
                        size={15}
                        className="text-blue-400"
                    />

                    <span
                        className="
                            text-sm
                            font-medium
                            text-blue-300
                        "
                    >

                        Azure GPT-5 Nano

                    </span>

                </div>

                {/* SQL */}

                <div
                    className="
                        hidden
                        xl:flex

                        items-center
                        gap-2

                        rounded-full

                        border
                        border-emerald-500/20

                        bg-emerald-500/10

                        px-4
                        py-2
                    "
                >

                    <ShieldCheck
                        size={15}
                        className="text-emerald-400"
                    />

                    <span
                        className="
                            text-sm
                            font-medium
                            text-emerald-300
                        "
                    >

                        SQL Server Online

                    </span>

                </div>

                {/* IA */}

                <div
                    className="
                        flex
                        items-center
                        gap-2

                        rounded-full

                        border
                        border-cyan-500/20

                        bg-cyan-500/10

                        px-4
                        py-2
                    "
                >

                    <Activity
                        size={15}
                        className="
                            text-cyan-400
                        "
                    />

                    <span
                        className="
                            text-sm
                            font-medium
                            text-cyan-300
                        "
                    >

                        IA Active

                    </span>

                </div>

                {/* DB */}

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

                        px-4
                        py-2
                    "
                >

                    <Database
                        size={15}
                        className="text-slate-400"
                    />

                    <span
                        className="
                            text-sm
                            text-slate-400
                        "
                    >

                        IMMO_AI

                    </span>

                </div>

                {/* Heure */}

                <div
                    className="
                        hidden
                        xl:flex

                        items-center
                        gap-2

                        rounded-full

                        border
                        border-white/10

                        bg-white/5

                        px-4
                        py-2
                    "
                >

                    <Clock3
                        size={15}
                        className="text-slate-400"
                    />

                    <span
                        className="
                            text-sm
                            text-slate-400
                        "
                    >

                        Synchronisé • {currentTime}

                    </span>

                </div>

            </div>

        </header>

    );

};

export default ChatHeader;