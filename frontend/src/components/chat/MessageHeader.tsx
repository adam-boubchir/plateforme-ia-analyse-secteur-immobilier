import {
  Bot,
  User,
  ShieldCheck,
} from "lucide-react";

type Props = {
  role: "user" | "assistant";
};

const MessageHeader = ({ role }: Props) => {

  const isUser = role === "user";

  return (

    <div
      className="
        flex
        items-center
        justify-between
        mb-5
      "
    >

      <div className="flex items-center gap-4">

        <div
          className={`
            h-12
            w-12
            rounded-2xl
            flex
            items-center
            justify-center
            shadow-lg
            ${
              isUser
                ? "bg-gradient-to-br from-blue-600 to-cyan-500 shadow-blue-500/30"
                : "bg-gradient-to-br from-emerald-500 to-teal-600 shadow-emerald-500/30"
            }
          `}
        >

          {

            isUser

              ? <User size={22} />

              : <Bot size={22} />

          }

        </div>

        <div>

          <div
            className="
              text-base
              font-semibold
              tracking-wide
            "
          >

            {

              isUser

                ? "Vous"

                : "Habitat AI"

            }

          </div>

          <div
            className="
              mt-1
              flex
              items-center
              gap-2
              text-xs
              text-gray-400
            "
          >

            {

              isUser

                ? "Utilisateur"

                : (

                  <>

                    <ShieldCheck
                      size={13}
                      className="text-emerald-400"
                    />

                    Assistant IA

                  </>

                )

            }

          </div>

        </div>

      </div>

      {

        !isUser && (

          <div
            className="
              rounded-full
              border
              border-emerald-500/20
              bg-emerald-500/10
              px-3
              py-1
              text-xs
              font-medium
              text-emerald-300
            "
          >

            En ligne

          </div>

        )

      }

    </div>

  );

};

export default MessageHeader;