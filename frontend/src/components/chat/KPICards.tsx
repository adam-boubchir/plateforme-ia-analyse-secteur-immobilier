import {
  Database,
  TrendingUp,
  TrendingDown,
  Sigma,
} from "lucide-react";

type Props = {
  rows: Record<string, unknown>[];
};

const KPICards = ({ rows }: Props) => {

  if (rows.length === 0) {
    return null;
  }

  const columns = Object.keys(rows[0]);

  const numericColumns = columns.filter(column =>
    rows.every(row => typeof row[column] === "number")
  );

  const firstNumericColumn = numericColumns[0];

  let average: number | null = null;
  let minimum: number | null = null;
  let maximum: number | null = null;

  if (firstNumericColumn) {

    const values = rows.map(
      row => Number(row[firstNumericColumn])
    );

    average =
      values.reduce((a, b) => a + b, 0) /
      values.length;

    minimum = Math.min(...values);

    maximum = Math.max(...values);

  }

  const formatValue = (
    value: number | null
  ) => {

    if (value === null) {

      return "-";

    }

    return value.toLocaleString(
      "fr-FR",
      {
        maximumFractionDigits: 2,
      }
    );

  };

  return (

    <section
      className="
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-4
        gap-7
        mb-10
      "
    >

      <Card
        title="Résultats"
        subtitle="Lignes retournées"
        value={rows.length.toLocaleString()}
        icon={
          <Database
            size={28}
            strokeWidth={2.2}
          />
        }
        color="cyan"
      />

      {

        firstNumericColumn && (

          <>

            <Card
              title="Moyenne"
              subtitle={firstNumericColumn}
              value={formatValue(average)}
              icon={
                <Sigma
                  size={28}
                  strokeWidth={2.2}
                />
              }
              color="violet"
            />

            <Card
              title="Maximum"
              subtitle={firstNumericColumn}
              value={formatValue(maximum)}
              icon={
                <TrendingUp
                  size={28}
                  strokeWidth={2.2}
                />
              }
              color="emerald"
            />

            <Card
              title="Minimum"
              subtitle={firstNumericColumn}
              value={formatValue(minimum)}
              icon={
                <TrendingDown
                  size={28}
                  strokeWidth={2.2}
                />
              }
              color="rose"
            />

          </>

        )

      }

    </section>

  );

};

type CardProps = {

  title: string;

  subtitle: string;

  value: string | number | null | undefined;

  icon: React.ReactNode;

  color:
    | "cyan"
    | "violet"
    | "emerald"
    | "rose";

};

function Card({

  title,

  subtitle,

  value,

  icon,

  color,

}: CardProps) {

  const styles = {

    cyan: {
      glow: "shadow-cyan-500/20",
      border: "border-cyan-500/15",
      bg: "from-cyan-500/20 via-cyan-500/5 to-transparent",
      icon: "text-cyan-300",
      line: "bg-cyan-400",
    },

    violet: {
      glow: "shadow-violet-500/20",
      border: "border-violet-500/15",
      bg: "from-violet-500/20 via-violet-500/5 to-transparent",
      icon: "text-violet-300",
      line: "bg-violet-400",
    },

    emerald: {
      glow: "shadow-emerald-500/20",
      border: "border-emerald-500/15",
      bg: "from-emerald-500/20 via-emerald-500/5 to-transparent",
      icon: "text-emerald-300",
      line: "bg-emerald-400",
    },

    rose: {
      glow: "shadow-rose-500/20",
      border: "border-rose-500/15",
      bg: "from-rose-500/20 via-rose-500/5 to-transparent",
      icon: "text-rose-300",
      line: "bg-rose-400",
    },

  };

  const s = styles[color];

  return (

    <div
      className={`
        group
        relative
        overflow-hidden
        rounded-[28px]
        border
        ${s.border}
        bg-[#181818]
        transition-all
        duration-500
        hover:-translate-y-2
        hover:shadow-2xl
        ${s.glow}
      `}
    >

      <div
        className={`
          h-1
          w-full
          ${s.line}
        `}
      />

      <div
        className={`
          absolute
          inset-0
          bg-gradient-to-br
          ${s.bg}
          opacity-70
        `}
      />

      <div
        className="
          relative
          z-10
          p-7
        "
      >

        <div
          className="
            flex
            items-start
            justify-between
          "
        >

          <div>

            <p
              className="
                text-xs
                uppercase
                tracking-[0.25em]
                text-gray-500
              "
            >

              {title}

            </p>

            <h2
              className="
                mt-5
                text-[42px]
                font-black
                tracking-tight
                text-white
              "
            >

              {value}

            </h2>

            <p
              className="
                mt-2
                text-sm
                text-gray-400
              "
            >

              {subtitle}

            </p>

          </div>

          <div
            className={`
              relative
              flex
              h-16
              w-16
              items-center
              justify-center
              rounded-2xl
              bg-white/5
              backdrop-blur-xl
              ${s.icon}
            `}
          >

            <div
              className="
                absolute
                inset-0
                rounded-2xl
                bg-white/5
                blur-lg
                group-hover:scale-125
                transition-all
                duration-500
              "
            />

            <div className="relative">

              {icon}

            </div>

          </div>

        </div>

      </div>

      <div
        className="
          absolute
          -right-14
          -bottom-14
          h-40
          w-40
          rounded-full
          bg-white/[0.03]
          blur-2xl
        "
      />

    </div>

  );

}

export default KPICards;