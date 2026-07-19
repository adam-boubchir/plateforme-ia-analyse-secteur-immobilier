import {
    GeoJSON,
    MapContainer,
    TileLayer,
    useMap,
} from "react-leaflet";
import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import type { GeoJsonObject } from "geojson";

interface MoroccoMapProps {
    onRegionSelect?: (
        region: {
            code: string;
            name: string;
        }
    ) => void;
}

function FitBounds({ data }: { data: GeoJsonObject }) {
    const map = useMap();

    useEffect(() => {
        const layer = L.geoJSON(data);

        map.fitBounds(layer.getBounds(), {
            padding: [60, 60],
            maxZoom: 6,
        });
    }, [data, map]);

    return null;
}

function MapController({
    mapRef,
}: {
    mapRef: React.MutableRefObject<L.Map | null>;
}) {
    const map = useMap();

    useEffect(() => {
        mapRef.current = map;
    }, [map, mapRef]);

    return null;
}

const defaultStyle: L.PathOptions = {
    color: "#2563EB",
    weight: 2,
    fillColor: "#60A5FA",
    fillOpacity: 0.75,
};

const hoverStyle: L.PathOptions = {
    color: "#1D4ED8",
    weight: 3,
    fillColor: "#2563EB",
    fillOpacity: 0.95,
};

const selectedStyle: L.PathOptions = {
    color: "#0F172A",
    weight: 3,
    fillColor: "#1D4ED8",
    fillOpacity: 1,
};

export default function MoroccoMap({
    onRegionSelect,
}: MoroccoMapProps) {

    const [geoJson, setGeoJson] =
        useState<GeoJsonObject | null>(null);

    const mapRef = useRef<L.Map | null>(null);

    const selectedLayer = useRef<L.Path | null>(null);

    useEffect(() => {

        fetch("/maps/morocco_regions.geojson")
            .then((res) => res.json())
            .then(setGeoJson)
            .catch(console.error);

    }, []);

    if (!geoJson) {
        return (
            <div className="flex h-full items-center justify-center bg-slate-100">
                Chargement de la carte...
            </div>
        );
    }

    return (
        <MapContainer
            center={[31.8, -7.1]}
            zoom={6}
            minZoom={5}
            maxZoom={10}
            zoomControl={false}
            attributionControl={false}
            style={{
                width: "100%",
                height: "100%",
            }}
        >

            <TileLayer
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />

            <MapController mapRef={mapRef} />

            <FitBounds data={geoJson} />

            <GeoJSON
                data={geoJson}
                style={defaultStyle}
                onEachFeature={(feature, layer) => {

                    const polygon = layer as L.Path;

                    const regionName =
                        feature.properties?.name_fr ??
                        feature.properties?.name ??
                        "Région";

                    const regionCode =
                        feature.properties?.code ?? "";

                    polygon.bindTooltip(regionName, {
                        sticky: true,
                        direction: "top",
                    });

                    polygon.on({

                        mouseover: () => {

                            if (selectedLayer.current !== polygon) {
                                polygon.setStyle(hoverStyle);
                            }

                        },

                        mouseout: () => {

                            if (selectedLayer.current !== polygon) {
                                polygon.setStyle(defaultStyle);
                            }

                        },

                        click: () => {

                            if (selectedLayer.current) {
                                selectedLayer.current.setStyle(defaultStyle);
                            }

                            polygon.setStyle(selectedStyle);

                            selectedLayer.current = polygon;

                            onRegionSelect?.({
                                code: regionCode,
                                name: regionName,
                            });

                            if (mapRef.current) {

                                const bounds = (
                                    polygon as L.Polygon
                                ).getBounds();

                                mapRef.current.flyToBounds(bounds, {
                                    padding: [60, 60],
                                    duration: 0.8,
                                });

                            }

                        },

                    });

                }}
            />

        </MapContainer>
    );
}