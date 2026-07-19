import axios from "axios";

/*
|--------------------------------------------------------------------------
| API
|--------------------------------------------------------------------------
*/

const api = axios.create({
    baseURL: "http://localhost:8000/api/map",
    headers: {
        "Content-Type": "application/json",
    },
});

/*
|--------------------------------------------------------------------------
| Types
|--------------------------------------------------------------------------
*/

export interface Region {
    id_region: number;
    code_region: number;
    code_iso: string;
    nom_region: string;
    nom_region_ar: string;
}

export interface RegionStatistics {
    region: string;
    nombre_provinces: number;
    nombre_logements: number;
    prix_moyen: number;
    indice_moyen: number;
}

export interface PriceHistory {
    annee: number;
    materiau: string;
    prix_moyen: number;
    indice: number;
}

export interface HousingStatistics {
    annee: number;
    type_habitat: string;
    type_indicateur: string;
    montant_mad: number;
    indice: number;
}

/*
|--------------------------------------------------------------------------
| Service
|--------------------------------------------------------------------------
*/

const mapService = {

    /*
    ------------------------------------------------------------------------
    | Toutes les régions
    ------------------------------------------------------------------------
    */

    async getRegions(): Promise<Region[]> {

        const { data } = await api.get("/regions");

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Une région par code ISO
    ------------------------------------------------------------------------
    */

    async getRegion(
        codeIso: string
    ): Promise<Region> {

        const { data } = await api.get(
            `/regions/code/${encodeURIComponent(codeIso)}`
        );

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Statistiques
    ------------------------------------------------------------------------
    */

    async getRegionStatistics(
        codeIso: string
    ): Promise<RegionStatistics> {

        const { data } = await api.get(
            `/regions/code/${encodeURIComponent(codeIso)}/statistics`
        );

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Prix
    ------------------------------------------------------------------------
    */

    async getPriceHistory(
        codeIso: string
    ): Promise<PriceHistory[]> {

        const { data } = await api.get(
            `/regions/code/${encodeURIComponent(codeIso)}/prices`
        );

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Habitat
    ------------------------------------------------------------------------
    */

    async getHousingStatistics(
        codeIso: string
    ): Promise<HousingStatistics[]> {

        const { data } = await api.get(
            `/regions/code/${encodeURIComponent(codeIso)}/housing`
        );

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | IA
    ------------------------------------------------------------------------
    */

    async askAI(
        codeIso: string,
        question: string,
    ): Promise<string> {

        const { data } = await api.post(
            "/ai/region",
            {
                code_iso: codeIso,
                question,
            }
        );

        return data.answer;

    },

};

export default mapService;