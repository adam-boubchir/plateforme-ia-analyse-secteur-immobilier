import { useMemo, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
  AreaChart,
  Area,
} from "recharts";

import {
  BarChart3,
  LineChart as LineChartIcon,
  PieChart as PieChartIcon,
  Activity,
  TrendingUp,
} from "lucide-react";

type Props = {
  rows: Record<string, unknown>[];
};

const COLORS = [
  "#3B82F6",
  "#06B6D4",
  "#14B8A6",
  "#10B981",
  "#84CC16",
  "#FACC15",
  "#F97316",
  "#EF4444",
  "#8B5CF6",
  "#EC4899",
];

const MAX_CHART_ROWS = 50;

const ChartViewer = ({ rows }: Props) => {

  const [chartType, setChartType] = useState<
    "bar" | "line" | "pie" | "area"
  >("bar");

  if (rows.length < 2) {

    return null;

  }

  const chartRows = useMemo(() => {

    return rows.slice(0, MAX_CHART_ROWS);

  }, [rows]);

  const columns = Object.keys(chartRows[0]);

  const numericColumns = columns.filter(column =>

    chartRows.every(

      row => typeof row[column] === "number"

    )

  );

  if (numericColumns.length === 0) {

    return null;

  }

  const numericColumn = numericColumns[0];

  const labelColumn = columns.find(

    column => column !== numericColumn

  );

  if (!labelColumn) {

    return null;

  }

  const isYear = chartRows.every(

    row => /^\d{4}$/.test(String(row[labelColumn]))

  );

  const total = chartRows.reduce(

    (sum, row) =>

      sum + Number(row[numericColumn]),

    0

  );

  const average = total / chartRows.length;

  const maximum = Math.max(

    ...chartRows.map(

      row => Number(row[numericColumn])

    )

  );

  const minimum = Math.min(

    ...chartRows.map(

      row => Number(row[numericColumn])

    )

  );

  const format = (value: number) =>

    value.toLocaleString("fr-FR", {

      maximumFractionDigits: 2,

    });

  const CustomTooltip = ({
    active,
    payload,
    label,
  }: any) => {

    if (

      active &&
      payload &&
      payload.length

    ) {

      return (

        <div
          className="
            rounded-2xl
            border
            border-white/10
            bg-[#171717]
            px-5
            py-4
            shadow-2xl
          "
        >

          <div className="font-semibold mb-2">

            {label}

          </div>

          <div
            className="
              text-cyan-400
              font-bold
            "
          >

            {format(
              payload[0].value
            )}

          </div>

        </div>

      );

    }

    return null;

  };
    return (

    <div
      className="
        mt-10
        rounded-[28px]
        border
        border-white/10
        bg-[#161616]
        overflow-hidden
        shadow-[0_0_60px_rgba(0,0,0,0.45)]
      "
    >

      {/* Header */}

      <div
        className="
          flex
          items-center
          justify-between
          px-8
          py-7
          border-b
          border-white/10
        "
      >

        <div>

          <h2
            className="
              text-2xl
              font-bold
              tracking-tight
            "
          >

            Visualisation des données

          </h2>

          <p
            className="
              mt-2
              text-sm
              text-gray-400
            "
          >

            Analyse graphique automatique

          </p>

        </div>

        <div
          className="
            flex
            gap-3
          "
        >

          <button

            onClick={() => setChartType("bar")}

            className={`
              flex
              items-center
              gap-2
              rounded-xl
              px-4
              py-2.5
              transition-all
              ${
                chartType === "bar"
                  ? "bg-blue-600 shadow-lg shadow-blue-500/30"
                  : "bg-[#222] hover:bg-[#2d2d2d]"
              }
            `}
          >

            <BarChart3 size={18} />

            Histogramme

          </button>

          <button

            disabled={!isYear}

            onClick={() => setChartType("line")}

            className={`
              flex
              items-center
              gap-2
              rounded-xl
              px-4
              py-2.5
              transition-all
              ${
                chartType === "line"
                  ? "bg-blue-600 shadow-lg shadow-blue-500/30"
                  : "bg-[#222] hover:bg-[#2d2d2d]"
              }

              ${
                !isYear
                  ? "opacity-40 cursor-not-allowed"
                  : ""
              }

            `}
          >

            <LineChartIcon size={18} />

            Courbe

          </button>

          <button

            onClick={() => setChartType("area")}

            className={`
              flex
              items-center
              gap-2
              rounded-xl
              px-4
              py-2.5
              transition-all
              ${
                chartType === "area"
                  ? "bg-blue-600 shadow-lg shadow-blue-500/30"
                  : "bg-[#222] hover:bg-[#2d2d2d]"
              }
            `}
          >

            <Activity size={18} />

            Surface

          </button>

          <button

            onClick={() => setChartType("pie")}

            className={`
              flex
              items-center
              gap-2
              rounded-xl
              px-4
              py-2.5
              transition-all
              ${
                chartType === "pie"
                  ? "bg-blue-600 shadow-lg shadow-blue-500/30"
                  : "bg-[#222] hover:bg-[#2d2d2d]"
              }
            `}
          >

            <PieChartIcon size={18} />

            Camembert

          </button>

        </div>

      </div>

      {/* KPI */}

      <div
        className="
          grid
          grid-cols-4
          gap-6
          px-8
          py-6
        "
      >

        <div
          className="
            rounded-2xl
            bg-[#1c1c1c]
            border
            border-white/10
            p-5
          "
        >

          <div className="text-sm text-gray-400">

            Valeur totale

          </div>

          <div
            className="
              mt-3
              text-3xl
              font-bold
            "
          >

            {format(total)}

          </div>

        </div>

        <div
          className="
            rounded-2xl
            bg-[#1c1c1c]
            border
            border-white/10
            p-5
          "
        >

          <div className="text-sm text-gray-400">

            Moyenne

          </div>

          <div
            className="
              mt-3
              text-3xl
              font-bold
              text-cyan-400
            "
          >

            {format(average)}

          </div>

        </div>
                <div
          className="
            rounded-2xl
            bg-[#1c1c1c]
            border
            border-white/10
            p-5
          "
        >

          <div className="text-sm text-gray-400">

            Maximum

          </div>

          <div
            className="
              mt-3
              text-3xl
              font-bold
              text-emerald-400
            "
          >

            {format(maximum)}

          </div>

        </div>

        <div
          className="
            rounded-2xl
            bg-[#1c1c1c]
            border
            border-white/10
            p-5
          "
        >

          <div className="text-sm text-gray-400">

            Minimum

          </div>

          <div
            className="
              mt-3
              text-3xl
              font-bold
              text-orange-400
            "
          >

            {format(minimum)}

          </div>

        </div>

      </div>

      <div
        className="
          h-[520px]
          px-8
          pb-8
        "
      >

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          {

            chartType === "bar" ? (

              <BarChart
                data={chartRows}
              >

                <defs>

                  <linearGradient
                    id="barGradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >

                    <stop
                      offset="0%"
                      stopColor="#3B82F6"
                    />

                    <stop
                      offset="100%"
                      stopColor="#06B6D4"
                    />

                  </linearGradient>

                </defs>

                <CartesianGrid
                  stroke="#2a2a2a"
                  vertical={false}
                />

                <XAxis
                  dataKey={labelColumn}
                  tick={{
                    fill: "#9CA3AF",
                    fontSize: 12,
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis
                  tick={{
                    fill: "#9CA3AF",
                    fontSize: 12,
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip
                  content={<CustomTooltip />}
                />

                <Bar
                  dataKey={numericColumn}
                  fill="url(#barGradient)"
                  radius={[10,10,0,0]}
                  animationDuration={900}
                />

              </BarChart>

            )

            : chartType === "line" ? (

              <LineChart
                data={chartRows}
              >

                <CartesianGrid
                  stroke="#2a2a2a"
                  vertical={false}
                />

                <XAxis
                  dataKey={labelColumn}
                  tick={{
                    fill:"#9CA3AF"
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis
                  tick={{
                    fill:"#9CA3AF"
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip
                  content={<CustomTooltip />}
                />

                <Line

                  type="monotone"

                  dataKey={numericColumn}

                  stroke="#3B82F6"

                  strokeWidth={4}

                  dot={{

                    r:4,

                    fill:"#3B82F6",

                  }}

                  activeDot={{

                    r:7,

                  }}

                  animationDuration={1000}

                />

              </LineChart>

            )

            : chartType === "area" ? (

              <AreaChart
                data={chartRows}
              >

                <defs>

                  <linearGradient
                    id="areaGradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >

                    <stop
                      offset="0%"
                      stopColor="#3B82F6"
                      stopOpacity={0.9}
                    />

                    <stop
                      offset="100%"
                      stopColor="#3B82F6"
                      stopOpacity={0}
                    />

                  </linearGradient>

                </defs>

                <CartesianGrid
                  stroke="#2a2a2a"
                  vertical={false}
                />

                <XAxis
                  dataKey={labelColumn}
                  axisLine={false}
                  tickLine={false}
                  tick={{
                    fill:"#9CA3AF"
                  }}
                />

                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{
                    fill:"#9CA3AF"
                  }}
                />

                <Tooltip
                  content={<CustomTooltip />}
                />

                <Area

                  type="monotone"

                  dataKey={numericColumn}

                  stroke="#3B82F6"

                  fill="url(#areaGradient)"

                  strokeWidth={4}

                  animationDuration={900}

                />

              </AreaChart>

            )

            : (

              <PieChart>

                <Pie

                  data={chartRows}

                  dataKey={numericColumn}

                  nameKey={labelColumn}

                  innerRadius={90}

                  outerRadius={170}

                  paddingAngle={3}

                  animationDuration={900}

                >

                  {

                    chartRows.map(

                      (_,index)=>(

                        <Cell

                          key={index}

                          fill={
                            COLORS[
                              index % COLORS.length
                            ]
                          }

                        />

                      )

                    )

                  }

                </Pie>

                <Legend/>

                <Tooltip
                  content={<CustomTooltip />}
                />

              </PieChart>

            )

          }

        </ResponsiveContainer>

      </div>

    </div>

  );

};

export default ChartViewer;