import {
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

import type {
    PriceAnalysisResponse,
    HousingAnalysisResponse,
} from "../../services/mapService";

type AnalysisResult =
    | PriceAnalysisResponse
    | HousingAnalysisResponse;

interface Props {
    result?: AnalysisResult;
}

export default function ChartsPanel({
    result,
}: Props) {

    if (!result || result.rows.length === 0) {
        return null;
    }

    const isPriceAnalysis =
        "materiau" in result.rows[0];

    const data = result.rows.map((row) => {

        if (isPriceAnalysis) {

            return {
                annee: row.annee,
                valeur1: "prix_moyen" in row ? row.prix_moyen ?? 0 : 0,
                valeur2: row.indice ?? 0,
            };

        }

        return {
            annee: row.annee,
            valeur1: "montant_mad" in row ? row.montant_mad ?? 0 : 0,
            valeur2: row.indice ?? 0,
        };

    });

    return (

        <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">

            <h2 className="mb-6 text-2xl font-bold text-white">

                {isPriceAnalysis
                    ? "Évolution des prix"
                    : "Évolution des indicateurs habitat"}

            </h2>

            <div className="h-[420px]">

                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >

                    <LineChart data={data}>

                        <CartesianGrid
                            stroke="#334155"
                            strokeDasharray="4 4"
                        />

                        <XAxis
                            dataKey="annee"
                            stroke="#94a3b8"
                            tick={{ fill: "#cbd5e1" }}
                        />

                        <YAxis
                            stroke="#94a3b8"
                            tick={{ fill: "#cbd5e1" }}
                        />

                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#0f172a",
                                border: "1px solid #334155",
                                borderRadius: "12px",
                                color: "#ffffff",
                            }}
                            formatter={(value) => {

                                const numeric =
                                    typeof value === "number"
                                        ? value
                                        : Number(value ?? 0);

                                return [
                                    numeric.toFixed(2),
                                    "",
                                ];

                            }}
                        />

                        <Legend />

                        <Line
                            type="monotone"
                            dataKey="valeur1"
                            name={
                                isPriceAnalysis
                                    ? "Prix moyen"
                                    : "Montant"
                            }
                            stroke="#3b82f6"
                            strokeWidth={3}
                            dot={{ r: 4 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="valeur2"
                            name="Indice"
                            stroke="#10b981"
                            strokeWidth={3}
                            dot={{ r: 4 }}
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

        </div>

    );

}