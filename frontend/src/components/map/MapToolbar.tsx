import {
    Search,
    Layers3,
    MapPinned,
    Building2,
    BarChart3,
    BrainCircuit,
    Download,
    LocateFixed,
} from "lucide-react";

const MapToolbar = () => {
    return (
        <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-3 shadow-md">

            {/* Recherche */}

            <div className="relative w-80">

                <Search
                    size={18}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                />

                <input
                    type="text"
                    placeholder="Rechercher une région..."
                    className="w-full rounded-lg border border-slate-200 py-2 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500"
                />

            </div>

            {/* Actions */}

            <div className="flex items-center gap-2">

                <button
                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm transition hover:bg-blue-50"
                    title="Couches"
                >
                    <Layers3 size={18} />
                    Couches
                </button>

                <button
                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm transition hover:bg-blue-50"
                    title="Régions"
                >
                    <MapPinned size={18} />
                    Régions
                </button>

                <button
                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm transition hover:bg-blue-50"
                    title="Logements"
                >
                    <Building2 size={18} />
                    Logements
                </button>

                <button
                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm transition hover:bg-blue-50"
                    title="Statistiques"
                >
                    <BarChart3 size={18} />
                    Statistiques
                </button>

                <button
                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm transition hover:bg-blue-50"
                    title="Analyse IA"
                >
                    <BrainCircuit size={18} />
                    IA
                </button>

                <button
                    className="rounded-lg border border-slate-200 p-2 transition hover:bg-blue-50"
                    title="Ma position"
                >
                    <LocateFixed size={18} />
                </button>

                <button
                    className="rounded-lg border border-slate-200 p-2 transition hover:bg-blue-50"
                    title="Exporter"
                >
                    <Download size={18} />
                </button>

            </div>

        </div>
    );
};

export default MapToolbar;