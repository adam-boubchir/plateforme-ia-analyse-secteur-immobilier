import type {
    PriceAnalysisResponse,
} from "../../services/mapService";

interface Props {
    result?: PriceAnalysisResponse;
}

export default function DashboardCards({
    result,
}: Props) {

    if (!result || result.rows.length === 0) {
        return null;
    }

    const totalResults = result.total;

    const averagePrice =
        result.rows.reduce(
            (sum, row) => sum + (row.prix_moyen ?? 0),
            0
        ) / result.rows.length;

    const averageIndex =
        result.rows.reduce(
            (sum, row) => sum + (row.indice ?? 0),
            0
        ) / result.rows.length;

    const latestYear = Math.max(
        ...result.rows.map((row) => row.annee)
    );

    const cards = [
        {
            title: "Nombre de résultats",
            value: totalResults.toLocaleString(),
        },
        {
            title: "Prix moyen",
            value: averagePrice.toFixed(2),
        },
        {
            title: "Indice moyen",
            value: averageIndex.toFixed(2),
        },
        {
            title: "Dernière année",
            value: latestYear,
        },
    ];

    return (

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

            {cards.map((card) => (

                <div
                    key={card.title}
                    className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-xl transition duration-300 hover:border-blue-500 hover:shadow-blue-900/40"
                >

                    <p className="text-sm uppercase tracking-wide text-slate-400">

                        {card.title}

                    </p>

                    <p className="mt-4 text-4xl font-bold text-white">

                        {card.value}

                    </p>

                </div>

            ))}

        </div>

    );

}