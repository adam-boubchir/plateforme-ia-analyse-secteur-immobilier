import {
  Sparkles,
  Database,
  ShieldCheck,
  Clock3,
  Building2,
} from "lucide-react";

const ChatHeader = () => {

  const currentTime = new Date().toLocaleTimeString(
    "fr-FR",
    {
      hour: "2-digit",
      minute: "2-digit",
    }
  );

  return (

    <header
      className="
        sticky
        top-0
        z-20
        h-24
        px-10
        backdrop-blur-xl
        bg-[#0d1117]/90
        border-b
        border-white/10
        flex
        items-center
        justify-between
      "
    >

      {/* Partie gauche */}

      <div className="flex items-center gap-5">

        <div
          className="
            h-14
            w-14
            rounded-2xl
            bg-gradient-to-br
            from-blue-600
            via-cyan-500
            to-blue-700
            flex
            items-center
            justify-center
            shadow-xl
            shadow-blue-600/25
          "
        >

          <Building2 size={28} />

        </div>

        <div>

          <div
            className="
              flex
              items-center
              gap-2
            "
          >

            <h1
              className="
                text-3xl
                font-bold
                tracking-tight
                text-white
              "
            >

              Immobilier AI

            </h1>

            <Sparkles
              size={18}
              className="text-cyan-400"
            />

          </div>

          <p
            className="
              mt-1
              text-sm
              text-gray-400
            "
          >

            Plateforme intelligente d'analyse du secteur immobilier

          </p>

        </div>

      </div>

      {/* Partie droite */}

      <div className="flex items-center gap-4">

        <div
          className="
            flex
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
            size={16}
            className="text-emerald-400"
          />

          <span
            className="
              text-sm
              font-medium
              text-emerald-300
            "
          >

            SQL Server connecté

          </span>

        </div>

        <div
          className="
            flex
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

          <Database
            size={16}
            className="text-blue-400"
          />

          <span
            className="
              text-sm
              font-medium
              text-blue-300
            "
          >

            IA Active

          </span>

        </div>

        <div
          className="
            flex
            items-center
            gap-2
            rounded-full
            border
            border-white/10
            bg-[#1b1b1b]
            px-4
            py-2
          "
        >

          <Clock3
            size={15}
            className="text-gray-400"
          />

          <span
            className="
              text-sm
              text-gray-400
            "
          >

            Synchronisé à {currentTime}

          </span>

        </div>

      </div>

    </header>

  );

};

export default ChatHeader;