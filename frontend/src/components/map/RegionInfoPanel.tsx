import {
    MapPinned,
    BrainCircuit,
    ArrowRight,
} from "lucide-react";

import StatisticsCards from "./StatisticsCards";

interface SelectedRegion {
    code: string;
    name: string;
}

interface RegionStatistics {
    nombre_provinces: number;
    nombre_logements: number;
    prix_moyen: number;
    indice_moyen: number;
}

interface RegionInfoPanelProps {
    selectedRegion?: SelectedRegion;
    statistics?: RegionStatistics;
}

export default function RegionInfoPanel({
    selectedRegion,
    statistics,
}: RegionInfoPanelProps) {
    return (
        <div className="flex h-full flex-col gap-5">

            {/* Région sélectionnée */}

            <div className="rounded-2xl border border-slate-100 bg-white p-6 shadow-lg">

                <div className="mb-5 flex items-center gap-3">

                    <MapPinned
                        size={24}
                        className="text-blue-600"
                    />

                    <h2 className="text-lg font-semibold text-slate-800">
                        Région sélectionnée
                    </h2>

                </div>

                {selectedRegion ? (
                    <>
                        <h1 className="text-2xl font-bold text-blue-700">
                            {selectedRegion.name}
                        </h1>

                        <p className="mt-3 text-slate-500">
                            Consultez les indicateurs immobiliers,
                            les prix des matériaux et les analyses IA
                            de cette région.
                        </p>
                    </>
                ) : (
                    <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-5">

                        <p className="text-slate-500">
                            Cliquez sur une région de la carte pour afficher
                            ses statistiques.
                        </p>

                    </div>
                )}

            </div>

            {/* Cartes statistiques */}

            <StatisticsCards
                region={selectedRegion}
                statistics={statistics}
            />

            {/* Assistant IA */}

            <div className="flex-1 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 p-6 text-white shadow-xl">

                <div className="mb-5 flex items-center gap-3">

                    <BrainCircuit size={28} />

                    <h2 className="text-xl font-semibold">
                        Assistant IA
                    </h2>

                </div>

                <p className="leading-7 text-blue-100">
                    Sélectionnez une région puis posez vos questions
                    concernant les données immobilières,
                    les matériaux de construction
                    et les indicateurs de l'habitat.
                </p>

                <div className="mt-6 rounded-xl bg-white/10 p-4">

                    <p className="italic text-blue-50">
                        « Quel est le prix moyen des matériaux de
                        construction dans cette région ? »
                    </p>

                </div>

                <button
                    className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3 font-semibold text-blue-700 transition hover:scale-105"
                >
                    Poser une question à l'IA

                    <ArrowRight size={18} />
                </button>

            </div>

        </div>
    );
}