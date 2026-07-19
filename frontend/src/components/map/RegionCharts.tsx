import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    BarChart,
    Bar,
} from "recharts";

interface SelectedRegion {
    code: string;
    name: string;
}

interface PriceHistory {
    annee: number;
    materiau: string;
    prix_moyen: number;
    indice: number;
}

interface HousingStatistic {
    annee: number;
    type_habitat: string;
    type_indicateur: string;
    montant_mad: number;
    indice: number;
}

interface RegionChartsProps {
    region?: SelectedRegion;
    prices?: PriceHistory[];
    housing?: HousingStatistic[];
}

export default function RegionCharts({
    region,
    prices = [],
    housing = [],
}: RegionChartsProps) {

    if (!region) {
        return (
            <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h2 className="mb-4 text-lg font-semibold">
                    Graphiques
                </h2>

                <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50">

                    <p className="text-slate-500">
                        Sélectionnez une région pour afficher les graphiques.
                    </p>

                </div>

            </div>
        );
    }

    const priceData = prices.map((item) => ({
        year: item.annee,
        value: item.prix_moyen,
    }));

    const housingData = housing.map((item) => ({
        name: item.type_habitat,
        value: item.montant_mad,
    }));

    return (
        <div className="space-y-6">

            {/* Evolution des prix */}

            <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h2 className="mb-5 text-lg font-semibold">
                    Evolution des prix des matériaux
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={280}
                >

                    <LineChart data={priceData}>

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="year" />

                        <YAxis />

                        <Tooltip />

                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#2563EB"
                            strokeWidth={3}
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

            {/* Habitat */}

            <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h2 className="mb-5 text-lg font-semibold">
                    Statistiques Habitat
                </h2>

                <ResponsiveContainer
                    width="100%"
                    height={280}
                >

                    <BarChart data={housingData}>

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="name" />

                        <YAxis />

                        <Tooltip />

                        <Bar
                            dataKey="value"
                            fill="#2563EB"
                            radius={[8, 8, 0, 0]}
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>
    );
}