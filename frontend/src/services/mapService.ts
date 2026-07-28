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
    code_region: string;
    code_iso: string;
    nom_region: string;
    nom_region_ar: string;
}

export interface Province {
    id_province: number;
    nom_province: string;
}

export interface Material {
    id: number;
    nom: string;
}

export interface Year {
    annee: number;
}

export interface RegionStatistics {
    region: string;
    nombre_provinces: number;
    prix_moyen?: number;
    indice_moyen?: number;
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
| Analyse
|--------------------------------------------------------------------------
*/

export interface PriceAnalysisRow {
    annee: number;
    materiau: string;
    prix_moyen?: number;
    indice?: number;
}

export interface PriceAnalysisResponse {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
    rows: PriceAnalysisRow[];
}

export interface PriceAnalysisRequest {
    analysis_type: "prices";
    region_id: number;
    province_id?: number;
    material_id?: number;
    year?: number;
    page?: number;
    page_size?: number;
}

export interface HousingAnalysisRow {
    annee: number;
    type_habitat: string;
    type_indicateur: string;
    montant_mad?: number;
    indice?: number;
}

export interface HousingAnalysisResponse {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
    rows: HousingAnalysisRow[];
}

export interface HousingAnalysisRequest {
    analysis_type: "housing";
    region_id: number;
    province_id?: number;
    year?: number;
    page?: number;
    page_size?: number;
}

/*
|--------------------------------------------------------------------------
| Service
|--------------------------------------------------------------------------
*/

const mapService = {

    /*
    ------------------------------------------------------------------------
    | Régions
    ------------------------------------------------------------------------
    */

    async getRegions(): Promise<Region[]> {

        const { data } = await api.get("/regions");

        return data;

    },

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
    | Provinces
    ------------------------------------------------------------------------
    */

    async getProvincesByRegion(
        codeIso: string
    ): Promise<Province[]> {

        const { data } = await api.get(
            `/regions/code/${encodeURIComponent(codeIso)}/provinces`
        );

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Matériaux
    ------------------------------------------------------------------------
    */

    async getMaterials(): Promise<Material[]> {

        const { data } = await api.get("/materials");

        return data;

    },

    /*
    ------------------------------------------------------------------------
    | Années
    ------------------------------------------------------------------------
    */

    async getAvailableYears(): Promise<Year[]> {

        const { data } = await api.get("/years");

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
    | Historique des prix
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
    | Analyse
    ------------------------------------------------------------------------
    */

    async analyzePrices(
        request: PriceAnalysisRequest
    ): Promise<PriceAnalysisResponse> {

        const { data } = await api.post(
            "/analysis",
            request
        );

        return data;

    },

    async analyzeHousing(
        request: HousingAnalysisRequest
    ): Promise<HousingAnalysisResponse> {

        const { data } = await api.post(
            "/analysis",
            request
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