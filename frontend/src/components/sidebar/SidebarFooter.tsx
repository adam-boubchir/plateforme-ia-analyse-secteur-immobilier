import {
    Settings,
    Cpu,
    ShieldCheck,
    Sparkles,
} from "lucide-react";

const SidebarFooter = () => {

    return (

        <footer
            className="
                border-t
                border-slate-700/40

                bg-gradient-to-b
                from-[#171717]
                to-[#111111]

                p-5
            "
        >

            {/* ================================================= */}
            {/* STATUS */}
            {/* ================================================= */}

            <div
                className="
                    rounded-2xl

                    border
                    border-white/10

                    bg-white/[0.03]

                    p-4

                    space-y-3
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-between
                    "
                >

                    <span
                        className="
                            text-xs
                            uppercase
                            tracking-[0.25em]

                            text-slate-500
                        "
                    >

                        Platform

                    </span>

                    <div
                        className="
                            flex
                            items-center
                            gap-2

                            rounded-full

                            bg-emerald-500/10

                            px-3
                            py-1

                            text-xs
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

                        Online

                    </div>

                </div>

                <div
                    className="
                        flex
                        items-center
                        gap-3
                    "
                >

                    <Cpu
                        size={18}
                        className="text-blue-400"
                    />

                    <div>

                        <div
                            className="
                                text-sm
                                font-semibold
                            "
                        >

                            Azure GPT-5 Nano

                        </div>

                        <div
                            className="
                                text-xs
                                text-slate-500
                            "
                        >

                            AI Model

                        </div>

                    </div>

                </div>

                <div
                    className="
                        flex
                        items-center
                        gap-3
                    "
                >

                    <ShieldCheck
                        size={18}
                        className="text-emerald-400"
                    />

                    <div>

                        <div
                            className="
                                text-sm
                                font-semibold
                            "
                        >

                            SQL Server Connected

                        </div>

                        <div
                            className="
                                text-xs
                                text-slate-500
                            "
                        >

                            Database

                        </div>

                    </div>

                </div>

            </div>

            {/* ================================================= */}
            {/* SETTINGS */}
            {/* ================================================= */}

            <button

                className="
                    mt-4

                    w-full

                    rounded-2xl

                    border
                    border-white/10

                    bg-[#1d1d1d]

                    px-4
                    py-3

                    flex
                    items-center
                    justify-center
                    gap-3

                    transition-all
                    duration-300

                    hover:bg-[#252525]
                    hover:border-blue-500/20
                "

            >

                <Settings size={18} />

                Paramètres

            </button>

            {/* ================================================= */}
            {/* VERSION */}
            {/* ================================================= */}

            <div
                className="
                    mt-5

                    text-center

                    text-xs

                    text-slate-500
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-center
                        gap-2
                    "
                >

                    <Sparkles
                        size={13}
                        className="text-cyan-400"
                    />

                    Immobilier AI Platform

                </div>

                <div className="mt-2">

                    Version 1.0.0

                </div>

                <div className="mt-1">

                    © 2026 Ministère de l'Habitat

                </div>

            </div>

        </footer>

    );

};

export default SidebarFooter;