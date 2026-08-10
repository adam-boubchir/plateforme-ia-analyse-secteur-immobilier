import { useState } from "react";
import {
    Clipboard,
    Check,
    ChevronDown,
    ChevronUp,
    Database,
} from "lucide-react";

type Props = {
    sql: string;
};

const SQLViewer = ({ sql }: Props) => {

    const [expanded, setExpanded] = useState(false);
    const [copied, setCopied] = useState(false);

    const copySql = async () => {

        await navigator.clipboard.writeText(sql);

        setCopied(true);

        setTimeout(() => {

            setCopied(false);

        }, 1500);

    };

    return (

        <div className="mt-8">

            {/* Header */}

            <button
                onClick={() => setExpanded(!expanded)}
                className="
                    w-full

                    flex
                    items-center
                    justify-between

                    rounded-xl

                    border
                    border-slate-700/40

                    bg-[#181818]

                    px-5
                    py-4

                    hover:bg-[#1d1d1d]

                    transition-all
                "
            >

                <div className="flex items-center gap-3">

                    <Database
                        size={16}
                        className="text-blue-400"
                    />

                    <span
                        className="
                            text-sm
                            font-medium
                            text-white
                        "
                    >
                        SQL Server
                    </span>

                </div>

                <div className="flex items-center gap-3">

                    <button
                        onClick={(e) => {

                            e.stopPropagation();

                            copySql();

                        }}
                        className="
                            flex
                            items-center
                            gap-2

                            rounded-lg

                            px-3
                            py-2

                            text-xs

                            hover:bg-white/5
                        "
                    >

                        {

                            copied

                                ? <Check size={15}/>

                                : <Clipboard size={15}/>

                        }

                        {

                            copied

                                ? "Copié"

                                : "Copier"

                        }

                    </button>

                    {

                        expanded

                            ? <ChevronUp size={18}/>

                            : <ChevronDown size={18}/>

                    }

                </div>

            </button>

            {

                expanded && (

                    <pre
                        className="
                            mt-3

                            overflow-x-auto

                            rounded-xl

                            border
                            border-slate-700/40

                            bg-[#0d1117]

                            p-6

                            text-[13px]

                            leading-7

                            text-slate-200

                            font-mono
                        "
                    >

                        <code>

                            {sql}

                        </code>

                    </pre>

                )

            }

        </div>

    );

};

export default SQLViewer;