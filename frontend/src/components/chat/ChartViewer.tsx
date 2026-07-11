import { useMemo, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

type Props = {
  rows: Record<string, unknown>[];
};

const COLORS = [
  "#3b82f6",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4",
  "#84cc16",
  "#ec4899",
];

const MAX_CHART_ROWS = 50;

const ChartViewer = ({ rows }: Props) => {

  const [chartType, setChartType] = useState<
    "bar" | "line" | "pie"
  >("bar");

  if (rows.length < 2) {

    return null;

  }

  const chartRows = useMemo(() => {

    return rows.slice(0, MAX_CHART_ROWS);

  }, [rows]);

  const columns = Object.keys(chartRows[0]);

  const numericColumns = columns.filter(column =>

    chartRows.every(row =>

      typeof row[column] === "number"

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

  const isYear = chartRows.every(row =>

    /^\d{4}$/.test(String(row[labelColumn]))

  );

  return (

    <div
      className="
        mt-6
        rounded-xl
        border
        border-gray-700
        bg-[#202020]
        p-5
      "
    >

      <div className="flex items-center justify-between mb-5">

        <h3 className="text-lg font-semibold">

          📊 Visualisation

        </h3>

        <div className="flex gap-2">

          <button

            onClick={() => setChartType("bar")}

            className={`px-3 py-2 rounded-lg text-sm transition ${
              chartType === "bar"
                ? "bg-blue-600"
                : "bg-[#2b2b2b] hover:bg-[#3a3a3a]"
            }`}

          >

            📊 Histogramme

          </button>

          <button

            onClick={() => setChartType("line")}

            disabled={!isYear}

            className={`px-3 py-2 rounded-lg text-sm transition ${
              chartType === "line"
                ? "bg-blue-600"
                : "bg-[#2b2b2b] hover:bg-[#3a3a3a]"
            } ${
              !isYear
                ? "opacity-40 cursor-not-allowed"
                : ""
            }`}

          >

            📈 Courbe

          </button>

          <button

            onClick={() => setChartType("pie")}

            className={`px-3 py-2 rounded-lg text-sm transition ${
              chartType === "pie"
                ? "bg-blue-600"
                : "bg-[#2b2b2b] hover:bg-[#3a3a3a]"
            }`}

          >

            🥧 Camembert

          </button>

        </div>

      </div>

      <p className="text-xs text-gray-400 mb-3">

        Visualisation limitée aux {MAX_CHART_ROWS} premières lignes.

      </p>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        {

          chartType === "line" && isYear ? (

            <LineChart data={chartRows}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey={labelColumn} />

              <YAxis />

              <Tooltip />

              <Line

                type="monotone"

                dataKey={numericColumn}

                stroke="#3b82f6"

                strokeWidth={3}

              />

            </LineChart>

          )

          : chartType === "pie" ? (

            <PieChart>

              <Pie

                data={chartRows}

                dataKey={numericColumn}

                nameKey={labelColumn}

                outerRadius={120}

                label

              >

                {

                  chartRows.map((_, index) => (

                    <Cell

                      key={index}

                      fill={

                        COLORS[

                          index % COLORS.length

                        ]

                      }

                    />

                  ))

                }

              </Pie>

              <Legend />

              <Tooltip />

            </PieChart>

          )

          : (

            <BarChart data={chartRows}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis

                dataKey={labelColumn}

                angle={-35}

                textAnchor="end"

                interval={0}

                height={80}

              />

              <YAxis />

              <Tooltip />

              <Bar

                dataKey={numericColumn}

                fill="#3b82f6"

                radius={[6, 6, 0, 0]}

              />

            </BarChart>

          )

        }

      </ResponsiveContainer>

    </div>

  );

};

export default ChartViewer;