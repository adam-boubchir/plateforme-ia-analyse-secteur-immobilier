import { Search, X } from "lucide-react";

type Props = {
    value: string;
    onChange: (value: string) => void;
};

const SearchConversation = ({
    value,
    onChange,
}: Props) => {

    return (

        <div className="px-5 py-5">

            <div
                className="
                    group
                    relative

                    overflow-hidden

                    rounded-2xl

                    border
                    border-slate-700/50

                    bg-gradient-to-br
                    from-[#202020]
                    to-[#171717]

                    shadow-lg

                    transition-all
                    duration-300

                    focus-within:border-cyan-500/40
                    focus-within:shadow-cyan-500/10
                "
            >

                {/* Halo */}

                <div
                    className="
                        pointer-events-none

                        absolute
                        -right-8
                        -top-8

                        h-24
                        w-24

                        rounded-full

                        bg-cyan-500/5

                        blur-2xl
                    "
                />

                {/* Search Icon */}

                <Search
                    size={18}
                    className="
                        absolute

                        left-4
                        top-1/2

                        -translate-y-1/2

                        text-slate-500

                        transition-colors

                        group-focus-within:text-cyan-400
                    "
                />

                {/* Input */}

                <input

                    value={value}

                    onChange={(e) =>
                        onChange(e.target.value)
                    }

                    placeholder="Rechercher une conversation..."

                    className="
                        h-12
                        w-full

                        bg-transparent

                        pl-11
                        pr-24

                        text-sm
                        text-white

                        placeholder:text-slate-500

                        outline-none
                    "

                />

                {/* Right side */}

                <div
                    className="
                        absolute

                        right-3
                        top-1/2

                        flex
                        items-center
                        gap-2

                        -translate-y-1/2
                    "
                >

                    {

                        value.length > 0 && (

                            <button

                                onClick={() =>
                                    onChange("")
                                }

                                className="
                                    flex
                                    h-7
                                    w-7
                                    items-center
                                    justify-center

                                    rounded-lg

                                    text-slate-400

                                    transition-all

                                    hover:bg-slate-700
                                    hover:text-white
                                "

                            >

                                <X size={15} />

                            </button>

                        )

                    }

                    <div
                        className="
                            hidden
                            lg:flex

                            items-center

                            rounded-lg

                            border
                            border-slate-700

                            bg-slate-800/60

                            px-2
                            py-1

                            text-[10px]
                            font-medium

                            tracking-wide

                            text-slate-400
                        "
                    >

                        Ctrl K

                    </div>

                </div>

            </div>

        </div>

    );

};

export default SearchConversation;