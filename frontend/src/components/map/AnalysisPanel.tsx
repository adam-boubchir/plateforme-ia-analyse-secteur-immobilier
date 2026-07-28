import { useEffect, useState } from "react";

import mapService from "../../services/mapService";

import type {
    Province,
    Material,
    Year,
} from "../../services/mapService";

interface SelectedRegion {
    code: string;
    name: string;
}

interface Props {
    selectedRegion?: SelectedRegion;

    onAnalyze?: (params: {
        regionCode: string;
        zoneType: "region" | "province";
        provinceId?: number;
        materialId?: number;
        year?: number;
        analysisType: "prices" | "housing" | "both";
    }) => void;
}

export default function AnalysisPanel({
    selectedRegion,
    onAnalyze,
}: Props) {

    const [provinces, setProvinces] =
        useState<Province[]>([]);

    const [materials, setMaterials] =
        useState<Material[]>([]);

    const [years, setYears] =
        useState<Year[]>([]);

    const [zoneType, setZoneType] =
        useState<"region" | "province">("region");

    const [selectedProvince, setSelectedProvince] =
        useState<number | "">("");

    const [selectedMaterial, setSelectedMaterial] =
        useState<number | "">("");

    const [selectedYear, setSelectedYear] =
        useState<number | "">("");

    const [analysisType, setAnalysisType] =
        useState<"prices" | "housing" | "both">("prices");

    useEffect(() => {

        if (analysisType === "housing") {

            setSelectedMaterial("");

        }

    }, [analysisType]);

    useEffect(() => {

        async function loadData() {

            if (!selectedRegion) {

                setProvinces([]);

                return;

            }
            

            try {

                const [
                    provincesData,
                    materialsData,
                    yearsData,
                ] = await Promise.all([

                    mapService.getProvincesByRegion(
                        selectedRegion.code
                    ),

                    mapService.getMaterials(),

                    mapService.getAvailableYears(),

                ]);

                setProvinces(provincesData);

                setMaterials(materialsData);

                setYears(yearsData);

            }

            catch (error) {

                console.error(error);

            }

        }

        loadData();

        setZoneType("region");

        setSelectedProvince("");

        setSelectedMaterial("");

        setSelectedYear("");

    }, [selectedRegion]);

    return (

    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

        <h2 className="mb-6 text-xl font-bold text-white">

            Analyse

        </h2>

        {!selectedRegion && (

            <p className="text-slate-400">

                Sélectionnez une région sur la carte.

            </p>

        )}

        {selectedRegion && (

            <>

                {/* Région sélectionnée */}

                <div className="mb-6">

                    <p className="text-sm text-slate-400">

                        Région sélectionnée

                    </p>

                    <p className="mt-1 text-lg font-semibold">

                        {selectedRegion.name}

                    </p>

                </div>

                {/* Zone */}

                <div className="mb-6">

                    <label className="mb-2 block font-medium">

                        Zone d'étude

                    </label>

                    <div className="space-y-2">

                        <label className="flex items-center gap-2">

                            <input
                                type="radio"
                                checked={zoneType === "region"}
                                onChange={() => setZoneType("region")}
                            />

                            Toute la région

                        </label>

                        <label className="flex items-center gap-2">

                            <input
                                type="radio"
                                checked={zoneType === "province"}
                                onChange={() => setZoneType("province")}
                            />

                            Province

                        </label>

                    </div>

                </div>

                {/* Province */}

                {zoneType === "province" && (

                    <div className="mb-6">

                        <label className="mb-2 block">

                            Province

                        </label>

                        <select
                            className="w-full rounded-lg bg-slate-800 p-2"
                            value={selectedProvince}
                            onChange={(e) =>
                                setSelectedProvince(Number(e.target.value))
                            }
                        >

                            <option value="">

                                Toutes

                            </option>

                            {provinces.map((province) => (

                                <option
                                    key={province.id_province}
                                    value={province.id_province}
                                >

                                    {province.nom_province}

                                </option>

                            ))}

                        </select>

                    </div>

                )}

                {/* Type d'analyse */}

                <div className="mb-6">

                    <label className="mb-2 block">

                        Type d'analyse

                    </label>

                    <select
                        className="w-full rounded-lg bg-slate-800 p-2"
                        value={analysisType}
                        onChange={(e) =>
                            setAnalysisType(
                                e.target.value as
                                    | "prices"
                                    | "housing"
                                    | "both"
                            )
                        }
                    >

                        <option value="prices">

                            Prix des matériaux

                        </option>

                        <option value="housing">

                            Habitat

                        </option>

                        <option value="both">

                            Prix + Habitat

                        </option>

                    </select>

                </div>

                {/* Matériau */}

                {(analysisType === "prices" ||
                    analysisType === "both") && (

                    <div className="mb-6">

                        <label className="mb-2 block">

                            Matériau

                        </label>

                        <select
                            className="w-full rounded-lg bg-slate-800 p-2"
                            value={selectedMaterial}
                            onChange={(e) =>
                                setSelectedMaterial(Number(e.target.value))
                            }
                        >

                            <option value="">

                                Tous les matériaux

                            </option>

                            {materials.map((material) => (

                                <option
                                    key={material.id}
                                    value={material.id}
                                >

                                    {material.nom}

                                </option>

                            ))}

                        </select>

                    </div>

                )}

                {/* Année */}

                <div className="mb-6">

                    <label className="mb-2 block">

                        Année

                    </label>

                    <select
                        className="w-full rounded-lg bg-slate-800 p-2"
                        value={selectedYear}
                        onChange={(e) =>
                            setSelectedYear(Number(e.target.value))
                        }
                    >

                        <option value="">

                            Toutes

                        </option>

                        {years.map((year) => (

                            <option
                                key={year.annee}
                                value={year.annee}
                            >

                                {year.annee}

                            </option>

                        ))}

                    </select>

                </div>

                {/* Bouton */}

                <button
                    className="w-full rounded-xl bg-blue-600 py-3 font-semibold transition hover:bg-blue-700"
                    onClick={() => {

                        if (!selectedRegion) return;

                        onAnalyze?.({

                            regionCode: selectedRegion.code,

                            zoneType,

                            provinceId:
                                zoneType === "province"
                                    ? Number(selectedProvince)
                                    : undefined,

                            materialId:
                                (analysisType === "prices" ||
                                    analysisType === "both") &&
                                selectedMaterial !== ""
                                    ? Number(selectedMaterial)
                                    : undefined,

                            year:
                                selectedYear === ""
                                    ? undefined
                                    : Number(selectedYear),

                            analysisType,

                        });

                    }}
                >

                    Analyser

                </button>

            </>

        )}

    </div>

);
}