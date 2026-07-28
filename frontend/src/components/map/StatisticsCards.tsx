import {
    BarChart3,
    Layers3,
    MapPinned,
} from "lucide-react";

interface SelectedRegion {
    code: string;
    name: string;
}

interface Statistics {
    nombre_provinces: number;
    prix_moyen?: number;
    indice_moyen?: number;
}

interface StatisticsCardsProps {
    region?: SelectedRegion;
    statistics?: Statistics;
}

export default function StatisticsCards({
    region,
    statistics,
}: StatisticsCardsProps) {

    const cards = [
        {
            title: "Provinces",
            value: statistics?.nombre_provinces ?? "—",
            icon: MapPinned,
        },
        {
            title: "Prix moyen",
            value:
                statistics?.prix_moyen !== undefined &&
                statistics.prix_moyen !== null
                    ? `${statistics.prix_moyen.toFixed(2)} MAD`
                    : "—",
            icon: BarChart3,
        },
        {
            title: "Indice moyen",
            value:
                statistics?.indice_moyen !== undefined &&
                statistics.indice_moyen !== null
                    ? statistics.indice_moyen.toFixed(2)
                    : "—",
            icon: Layers3,
        },
    ];

    return (
        <div className="grid grid-cols-3 gap-4">

            {cards.map((card) => {

                const Icon = card.icon;

                return (

                    <div
                        key={card.title}
                        className="rounded-2xl bg-white p-5 shadow-lg transition hover:shadow-xl"
                    >

                        <Icon
                            className="mb-3 text-blue-600"
                            size={24}
                        />

                        <p className="text-sm text-slate-500">
                            {card.title}
                        </p>

                        <h2 className="mt-2 text-2xl font-bold text-slate-800">
                            {region ? card.value : "—"}
                        </h2>

                    </div>

                );

            })}

        </div>
    );

}