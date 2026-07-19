import { useEffect, useState } from "react";

import MoroccoMap from "../components/map/MoroccoMap";
import RegionInfoPanel from "../components/map/RegionInfoPanel";
import RegionCharts from "../components/map/RegionCharts";

import mapService from "../services/mapService";

import type {
    RegionStatistics,
    PriceHistory,
    HousingStatistics,
} from "../services/mapService";

interface SelectedRegion {
    code: string;
    name: string;
}

export default function MapPage() {

    const [selectedRegion, setSelectedRegion] =
        useState<SelectedRegion>();

    const [statistics, setStatistics] =
        useState<RegionStatistics>();

    const [prices, setPrices] =
        useState<PriceHistory[]>([]);

    const [housing, setHousing] =
        useState<HousingStatistics[]>([]);

    useEffect(() => {

        if (!selectedRegion) return;

        const region = selectedRegion;

        async function loadRegionData() {

            try {

                const [
                    statisticsData,
                    pricesData,
                    housingData,
                ] = await Promise.all([

                    mapService.getRegionStatistics(
                        region.code
                    ),

                    mapService.getPriceHistory(
                        region.code
                    ),

                    mapService.getHousingStatistics(
                        region.code
                    ),

                ]);

                setStatistics(statisticsData);
                setPrices(pricesData);
                setHousing(housingData);

            } catch (error) {

                console.error(
                    "Erreur lors du chargement des données :",
                    error
                );

            }

        }

        loadRegionData();

    }, [selectedRegion]);

    return (

        <div className="h-screen bg-slate-100">

            <div className="grid h-full grid-cols-12 gap-6 p-6">

                {/* Carte */}

                <div className="col-span-7 overflow-hidden rounded-3xl bg-white shadow-xl">

                    <MoroccoMap
                        onRegionSelect={setSelectedRegion}
                    />

                </div>

                {/* Informations */}

                <div className="col-span-5 flex flex-col gap-6">

                    <RegionInfoPanel
                        selectedRegion={selectedRegion}
                        statistics={statistics}
                    />

                    <RegionCharts
                        region={selectedRegion}
                        prices={prices}
                        housing={housing}
                    />

                </div>

            </div>

        </div>

    );

}