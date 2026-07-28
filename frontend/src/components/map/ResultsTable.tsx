import type {
    PriceAnalysisResponse,
    HousingAnalysisResponse,
} from "../../services/mapService";

import Pagination from "./Pagination";

type AnalysisResult =
    | PriceAnalysisResponse
    | HousingAnalysisResponse;

interface Props {
    result?: AnalysisResult;
    onPageChange?: (page: number) => void;
}

export default function ResultsTable({
    result,
    onPageChange,
}: Props) {

    if (!result) {
        return null;
    }

    const isPriceAnalysis =
        result.rows.length === 0 ||
        "materiau" in result.rows[0];

    return (

        <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

            <h2 className="mb-4 text-xl font-bold text-white">
                Résultats
            </h2>

            <div className="mb-4 text-sm text-slate-400">
                {result.total} résultat{result.total > 1 ? "s" : ""}
            </div>

            {result.rows.length === 0 ? (

                <div className="rounded-xl border border-dashed border-slate-700 p-8 text-center text-slate-400">
                    Aucun résultat trouvé.
                </div>

            ) : (

                <div className="overflow-x-auto">

                    <table className="min-w-full border-collapse">

                        <thead>

                            {isPriceAnalysis ? (

                                <tr className="border-b border-slate-700 bg-slate-800">

                                    <th className="p-3 text-left text-slate-300">
                                        Année
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Matériau
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Prix moyen
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Indice
                                    </th>

                                </tr>

                            ) : (

                                <tr className="border-b border-slate-700 bg-slate-800">

                                    <th className="p-3 text-left text-slate-300">
                                        Année
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Type habitat
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Type indicateur
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Montant
                                    </th>

                                    <th className="p-3 text-left text-slate-300">
                                        Indice
                                    </th>

                                </tr>

                            )}

                        </thead>

                        <tbody>

                            {result.rows.map((row, index) => (

                                isPriceAnalysis ? (

                                    <tr
                                        key={index}
                                        className="border-b border-slate-800 hover:bg-slate-800"
                                    >

                                        <td className="p-3 text-white">
                                            {row.annee}
                                        </td>

                                        <td className="p-3 text-white">
                                            {"materiau" in row ? row.materiau : "-"}
                                        </td>

                                        <td className="p-3 text-white">
                                            {"prix_moyen" in row && row.prix_moyen != null
                                                ? `${row.prix_moyen.toFixed(2)} MAD`
                                                : "—"}
                                        </td>

                                        <td className="p-3 text-white">
                                            {row.indice ?? "—"}
                                        </td>

                                    </tr>

                                ) : (

                                    <tr
                                        key={index}
                                        className="border-b border-slate-800 hover:bg-slate-800"
                                    >

                                        <td className="p-3 text-white">
                                            {row.annee}
                                        </td>

                                        <td className="p-3 text-white">
                                            {"type_habitat" in row ? row.type_habitat : "-"}
                                        </td>

                                        <td className="p-3 text-white">
                                            {"type_indicateur" in row ? row.type_indicateur : "-"}
                                        </td>

                                        <td className="p-3 text-white">
                                            {"montant_mad" in row && row.montant_mad != null
                                                ? `${row.montant_mad.toFixed(2)} MAD`
                                                : "—"}
                                        </td>

                                        <td className="p-3 text-white">
                                            {row.indice ?? "—"}
                                        </td>

                                    </tr>

                                )

                            ))}

                        </tbody>

                    </table>

                </div>

            )}

            <div className="mt-6">

                <Pagination
                    page={result.page}
                    pageSize={result.page_size}
                    total={result.total}
                    onPageChange={(page) => {
                        onPageChange?.(page);
                    }}
                />

            </div>

        </div>

    );

}