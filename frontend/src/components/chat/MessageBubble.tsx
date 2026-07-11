import { useState } from "react";

import { Clipboard, Check } from "lucide-react";

import SQLResultTable from "./SQLResultTable";

import KPICards from "./KPICards";

import ChartViewer from "./ChartViewer";

type Props = {
  role: "user" | "assistant";
  content: string;
  sql?: string | null;
  rows?: unknown[];
};

const MessageBubble = ({
  role,
  content,
  sql,
  rows,
}: Props) => {

  const isUser = role === "user";

  const [showSql, setShowSql] = useState(false);

  const [copied, setCopied] = useState(false);

  const copySql = async () => {

    if (!sql) return;

    await navigator.clipboard.writeText(sql);

    setCopied(true);

    setTimeout(() => {

      setCopied(false);

    }, 2000);

  };

  return (

    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`
          max-w-5xl
          rounded-2xl
          px-6
          py-4
          shadow-md
          whitespace-pre-wrap
          ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-[#2f2f2f] text-white"
          }
        `}
      >

        {/* Réponse */}

        <div>

          {content}

        </div>

        {/* SQL */}

        {

          !isUser && sql && (

            <div className="mt-5 border-t border-gray-600 pt-4">

              <button

                onClick={() =>

                  setShowSql(!showSql)

                }

                className="text-blue-400 hover:text-blue-300 text-sm"

              >

                {

                  showSql

                    ? "Masquer le SQL"

                    : "Afficher le SQL"

                }

              </button>

              {

                showSql && (

                  <div
                    className="
                      mt-4
                      rounded-xl
                      overflow-hidden
                      border
                      border-gray-700
                    "
                  >

                    <div
                      className="
                        flex
                        items-center
                        justify-between
                        bg-[#1f1f1f]
                        px-4
                        py-2
                        border-b
                        border-gray-700
                      "
                    >

                      <span className="text-sm font-medium text-gray-300">

                        SQL généré

                      </span>

                      <button

                        onClick={copySql}

                        className="
                          flex
                          items-center
                          gap-2
                          text-sm
                          text-gray-300
                          hover:text-white
                          transition
                        "

                      >

                        {

                          copied

                            ? <Check size={16} />

                            : <Clipboard size={16} />

                        }

                        {

                          copied

                            ? "Copié !"

                            : "Copier"

                        }

                      </button>

                    </div>

                    <pre
                      className="
                        bg-[#151515]
                        text-green-400
                        p-5
                        overflow-x-auto
                        text-sm
                        leading-6
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

          )

        }

        {/* Tableau */}

        {
          !isUser &&
          rows &&
          rows.length > 0 && (

            <>

              <KPICards
                rows={rows as Record<string, unknown>[]}
              />

              <ChartViewer
                rows={rows as Record<string, unknown>[]}
              />

              <div className="mt-2 text-sm text-gray-400">

                📊 {rows.length} ligne(s) retournée(s)

              </div>

              <SQLResultTable
                rows={rows as Record<string, unknown>[]}
              />

            </>

          )

        }
      </div>

    </div>

  );

};

export default MessageBubble;