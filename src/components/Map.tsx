import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Coordinate {
  lat: number;
  lng: number;
}

interface MapProps {
  coordinates: Coordinate[];
}

const Map: React.FC<MapProps> = ({ coordinates }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletMapRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    // Destroy previous map if it exists
    if (leafletMapRef.current) {
      leafletMapRef.current.remove();
    }

    // Initialize map
    const map = L.map(mapRef.current).setView([20.0, 0.0], 2);
    leafletMapRef.current = map;

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    // Draw route if coordinates exist
    if (coordinates.length > 0) {
      const latLngs = coordinates.map((coord) => [coord.lat, coord.lng]) as [number, number][];
      const bounds = L.latLngBounds(latLngs);
      L.polyline(latLngs, { color: 'green', weight: 4 }).addTo(map);
      map.fitBounds(bounds, { padding: [50, 50] });
    }

  }, [coordinates]);

  return <div id="trip-map" ref={mapRef} className="w-full h-[400px] rounded shadow border" />;
};

export default Map;
