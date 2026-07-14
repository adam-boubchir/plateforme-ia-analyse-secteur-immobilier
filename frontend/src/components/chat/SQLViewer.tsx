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

    }, 2000);

  };

  return (

    <div className="mt-10">

      <button

        onClick={() => setExpanded(!expanded)}

        className="
          w-full
          rounded-2xl
          border
          border-white/10
          bg-[#1d1d1d]
          hover:bg-[#252525]
          transition-all
          duration-200
          px-6
          py-5
          flex
          items-center
          justify-between
        "

      >

        <div className="flex items-center gap-3">

          <div
            className="
              h-10
              w-10
              rounded-xl
              bg-blue-600/20
              flex
              items-center
              justify-center
            "
          >

            <Database
              size={18}
              className="text-blue-400"
            />

          </div>

          <div className="text-left">

            <div className="font-semibold">

              SQL généré

            </div>

            <div className="text-xs text-gray-400">

              Cliquez pour afficher la requête

            </div>

          </div>

        </div>

        {

          expanded

            ? <ChevronUp size={20} />

            : <ChevronDown size={20} />

        }

      </button>

      {

        expanded && (

          <div
            className="
              mt-4
              rounded-2xl
              overflow-hidden
              border
              border-white/10
              shadow-xl
            "
          >

            <div
              className="
                flex
                items-center
                justify-between
                bg-[#181818]
                px-6
                py-4
                border-b
                border-white/10
              "
            >

              <div className="flex items-center gap-3">

                <span
                  className="
                    rounded-full
                    bg-blue-600
                    px-3
                    py-1
                    text-xs
                    font-semibold
                  "
                >

                  SQL

                </span>

                <span className="text-sm text-gray-400">

                  Microsoft SQL Server

                </span>

              </div>

              <button

                onClick={copySql}

                className="
                  flex
                  items-center
                  gap-2
                  rounded-xl
                  px-4
                  py-2
                  hover:bg-[#252525]
                  transition
                "

              >

                {

                  copied

                    ? <Check size={17} />

                    : <Clipboard size={17} />

                }

                {

                  copied

                    ? "Copié"

                    : "Copier"

                }

              </button>

            </div>

            <pre
              className="
                bg-[#0d1117]
                text-green-400
                overflow-x-auto
                p-7
                text-[14px]
                leading-8
                font-mono
              "
            >

              <code>

                {sql}

              </code>

            </pre>

          </div>

        )

      }

    </div>

  );

};

export default SQLViewer;