import MessageHeader from "./MessageHeader";
import MessageContent from "./MessageContent";
import SQLViewer from "./SQLViewer";

import KPICards from "./KPICards";
import ChartViewer from "./ChartViewer";
import SQLResultTable from "./SQLResultTable";

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

  if (isUser) {

    return (

      <div className="flex justify-end">

        <div
          className="
            max-w-3xl
            rounded-[28px]
            bg-gradient-to-br
            from-blue-600
            to-blue-500
            px-7
            py-5
            shadow-2xl
            shadow-blue-500/20
          "
        >

          <MessageHeader role={role} />

          <div className="mt-4">

            <MessageContent
              content={content}
            />

          </div>

        </div>

      </div>

    );

  }

  return (

    <div
      className="
        rounded-[30px]
        border
        border-white/10
        bg-[#181818]
        shadow-2xl
        overflow-hidden
      "
    >

      {/* Header */}

      <div
        className="
          px-8
          py-6
          border-b
          border-white/10
          bg-gradient-to-r
          from-[#181818]
          to-[#202020]
        "
      >

        <MessageHeader role={role} />

      </div>

      {/* Contenu */}

      <div className="px-8 py-7">

        <MessageContent
          content={content}
        />

      </div>

      {

        sql && (

          <div
            className="
              px-8
              pb-7
            "
          >

            <SQLViewer
              sql={sql}
            />

          </div>

        )

      }

      {

        rows &&
        rows.length > 0 && (

          <>

            <div
              className="
                border-t
                border-white/10
                px-8
                py-7
              "
            >

              <KPICards
                rows={
                  rows as Record<
                    string,
                    unknown
                  >[]
                }
              />

            </div>

            <div
              className="
                px-8
                pb-8
              "
            >

              <ChartViewer
                rows={
                  rows as Record<
                    string,
                    unknown
                  >[]
                }
              />

            </div>

            <div
              className="
                px-8
                pb-3
                text-sm
                text-gray-400
                flex
                items-center
                justify-between
              "
            >

              <span>

                {rows.length.toLocaleString()} ligne(s)

              </span>

              <span>

                Résultat SQL

              </span>

            </div>

            <div className="px-8 pb-8">

              <SQLResultTable
                rows={
                  rows as Record<
                    string,
                    unknown
                  >[]
                }
              />

            </div>

          </>

        )

      }

    </div>

  );

};

export default MessageBubble;