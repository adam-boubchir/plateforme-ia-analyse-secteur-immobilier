import { useEffect, useState } from "react";

import MoroccoMap from "../components/map/MoroccoMap";
import RegionInfoPanel from "../components/map/RegionInfoPanel";
import AnalysisPanel from "../components/map/AnalysisPanel";
import ResultsTable from "../components/map/ResultsTable";
import ChartsPanel from "../components/map/ChartsPanel";

import mapService from "../services/mapService";

import type {
    PriceAnalysisResponse,
    HousingAnalysisResponse,
    RegionStatistics,
} from "../services/mapService";

interface SelectedRegion {
    code: string;
    name: string;
}

type AnalysisResult =
    | PriceAnalysisResponse
    | HousingAnalysisResponse;

export default function MapPage() {

    const [selectedRegion, setSelectedRegion] =
        useState<SelectedRegion>();

    const [statistics, setStatistics] =
        useState<RegionStatistics>();

    const [analysisResult, setAnalysisResult] =
        useState<AnalysisResult>();

    const [lastAnalysisParams, setLastAnalysisParams] = useState<{
        regionCode: string;
        zoneType: "region" | "province";
        provinceId?: number;
        materialId?: number;
        year?: number;
        analysisType: "prices" | "housing" | "both";
    }>();

    /*
    ------------------------------------------------------------------------
    | Charger les statistiques
    ------------------------------------------------------------------------
    */

    useEffect(() => {

        if (!selectedRegion) {

            setStatistics(undefined);

            return;

        }

        const regionCode = selectedRegion.code;

        async function loadStatistics() {

            try {

                const data =
                    await mapService.getRegionStatistics(
                        regionCode
                    );

                setStatistics(data);

            } catch (error) {

                console.error(error);

                setStatistics(undefined);

            }

        }

        loadStatistics();

    }, [selectedRegion]);

    /*
    ------------------------------------------------------------------------
    | Analyse
    ------------------------------------------------------------------------
    */

    async function handleAnalyze(params: {
        regionCode: string;
        zoneType: "region" | "province";
        provinceId?: number;
        materialId?: number;
        year?: number;
        analysisType: "prices" | "housing" | "both";
    }) {

        try {

            setLastAnalysisParams(params);

            const region =
                await mapService.getRegion(
                    params.regionCode
                );

            let result;

            if (params.analysisType === "prices") {

                result =
                    await mapService.analyzePrices({

                        analysis_type: "prices",

                        region_id: region.id_region,

                        province_id:
                            params.zoneType === "province"
                                ? params.provinceId
                                : undefined,

                        material_id: params.materialId,

                        year: params.year,

                        page: 1,

                        page_size: 20,

                    });

            }

            else if (params.analysisType === "housing") {

                result =
                    await mapService.analyzeHousing({

                        analysis_type: "housing",

                        region_id: region.id_region,

                        province_id:
                            params.zoneType === "province"
                                ? params.provinceId
                                : undefined,

                        year: params.year,

                        page: 1,

                        page_size: 20,

                    });

            }

            else {

                alert("L'analyse combinée sera disponible prochainement.");

                return;

            }

            setAnalysisResult(result);

        } catch (error) {

            console.error(error);

        }

    }

    async function handlePageChange(page: number) {

        if (!lastAnalysisParams) return;

        try {

            const region = await mapService.getRegion(
                lastAnalysisParams.regionCode
            );

            let result;

            if (lastAnalysisParams.analysisType === "prices") {

                result = await mapService.analyzePrices({

                    analysis_type: "prices",

                    region_id: region.id_region,

                    province_id:
                        lastAnalysisParams.zoneType === "province"
                            ? lastAnalysisParams.provinceId
                            : undefined,

                    material_id: lastAnalysisParams.materialId,

                    year: lastAnalysisParams.year,

                    page,

                    page_size: 20,

                });

            } else {

                result = await mapService.analyzeHousing({

                    analysis_type: "housing",

                    region_id: region.id_region,

                    province_id:
                        lastAnalysisParams.zoneType === "province"
                            ? lastAnalysisParams.provinceId
                            : undefined,

                    year: lastAnalysisParams.year,

                    page,

                    page_size: 20,

                });

            }

            setAnalysisResult(result);

        } catch (error) {

            console.error(error);

        }

    }

    return (

        <div
            className="
                h-full
                min-h-0
                overflow-y-auto
                overflow-x-hidden

                bg-[#0f172a]
                text-white

                scrollbar-thin
                scrollbar-thumb-slate-700
                scrollbar-track-transparent
            "
        >

            <div className="grid grid-cols-12 gap-6 p-6">

                <div className="col-span-7 overflow-hidden rounded-3xl bg-white shadow-2xl">

                    <MoroccoMap
                        onRegionSelect={setSelectedRegion}
                    />

                </div>

                <div className="col-span-5 flex flex-col gap-6">

                    <RegionInfoPanel
                        selectedRegion={selectedRegion}
                        statistics={statistics}
                    />

                    <AnalysisPanel
                        selectedRegion={selectedRegion}
                        onAnalyze={handleAnalyze}
                    />

                </div>

            </div>

            {analysisResult && (

                <div className="space-y-6 px-6 pb-6">

                    <ResultsTable
                        result={analysisResult}
                        onPageChange={handlePageChange}
                    />

                    <ChartsPanel
                        result={analysisResult}
                    />

                </div>

            )}

        </div>

    );

}