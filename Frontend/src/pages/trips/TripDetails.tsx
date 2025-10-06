import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TimelineChart from "./TimelineChart";
import RadarChart from "./RadarChart";
import SpeedChart from "./SpeedChart";
import { MapContainer, TileLayer, Marker, Tooltip, Polyline } from "react-leaflet";
import L from "leaflet";

const baseURL = import.meta.env.VITE_BASE_URL;

const TripDetails = () => {
  const { id } = useParams(); // unique_id from route
  const [tripDetails, setTripDetails] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("timeline");

  useEffect(() => {
    if (!id) return;

    const fetchTripDetails = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${baseURL}/trips/${id}`);
        if (!response.ok) throw new Error(`Error fetching trip ${id}: ${response.statusText}`);
        const data = await response.json();
        setTripDetails(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTripDetails();
  }, [id]);

  if (loading) return <p className="p-4">Loading trip details...</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;
  if (!tripDetails) return <p className="p-4">No trip found.</p>;

  // Extract coordinates if available
  let fromCoords: [number, number] | null = null;
  let toCoords: [number, number] | null = null;

  if (tripDetails.from && tripDetails.to) {
    const parseCoords = (loc: string) => {
      const parts = loc.split("→")[0].trim().replace(/[()]/g, "").split(",");
      return [parseFloat(parts[0]), parseFloat(parts[1])] as [number, number];
    };
    fromCoords = parseCoords(tripDetails.from);
    toCoords = parseCoords(tripDetails.to);
  }

  const getAddress = (location: string) => location?.split("→")[1]?.trim() || "";
  const fromAddress = getAddress(tripDetails.from);
  const toAddress = getAddress(tripDetails.to);

  const markerIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });

  return (
    <div className="flex min-h-screen bg-gray-50 p-6 gap-6">
      {/* Left panel with trip info */}
      <div className="w-1/3 bg-white rounded shadow p-4 space-y-4 overflow-y-auto">
        <h1 className="bg-gray-100 font-bold text-gray-700 px-4 py-1 rounded">
          Trip Details
        </h1>

        <div className="p-3 rounded border border-gray-200 space-y-1 text-sm">
          <div className="text-gray-800 font-semibold">
            Unique ID: {tripDetails.unique_id}
          </div>
          <div className="flex items-start">
            <span className="font-medium text-green-600 mr-2">From:</span>
            <span>{fromAddress}</span>
          </div>
          <div className="flex items-start">
            <span className="font-medium text-red-600 mr-2">To:</span>
            <span>{toAddress}</span>
          </div>
          <div>
            <span className="font-medium">Device ID:</span> {tripDetails.device_id}
          </div>
          <div>
            <span className="font-medium">Start Time:</span> {tripDetails.start_time}
          </div>
          <div>
            <span className="font-medium">End Time:</span> {tripDetails.end_time}
          </div>
        </div>
      </div>

      {/* Right panel with map and charts */}
      <div className="flex-1 space-y-6">
        <div className="h-96 w-full rounded shadow overflow-hidden">
          {fromCoords && toCoords ? (
            <MapContainer
              center={fromCoords}
              zoom={15}
              style={{ height: "100%", width: "100%" }}
            >
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

              <Marker position={fromCoords} icon={markerIcon}>
                <Tooltip sticky>{fromAddress}</Tooltip>
              </Marker>

              <Marker position={toCoords} icon={markerIcon}>
                <Tooltip sticky>{toAddress}</Tooltip>
              </Marker>

              <Polyline positions={[fromCoords, toCoords]} color="blue" weight={4} />
            </MapContainer>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              No map data available
            </div>
          )}
        </div>

        {/* Tabs for Timeline, Analytics, Speed */}
        <div className="bg-white shadow rounded">
          <div className="flex border-b">
            {["timeline", "analytics", "speed"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 text-sm ${
                  activeTab === tab
                    ? "border-b-2 border-green-600 text-green-600"
                    : "text-gray-600"
                }`}
              >
                {tab === "timeline"
                  ? "Timeline"
                  : tab === "analytics"
                  ? "Overall Analytics"
                  : "Speeding Analysis"}
              </button>
            ))}
          </div>
          <div className="p-4">
            {activeTab === "timeline" && <TimelineChart />}
            {activeTab === "analytics" && <RadarChart />}
            {activeTab === "speed" && <SpeedChart />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripDetails;
