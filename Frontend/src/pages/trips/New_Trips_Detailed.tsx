import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const baseURL = import.meta.env.VITE_BASE_URL;

// Fix default marker icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

interface TripInfo {
  unique_id: string;
  name: string;
  start_location: string;
  end_location: string;
  start_time: string;
  end_time: string;
  track_id?: string;
  avg_efficiency?: number;
}

interface DrivingTrips {
  labels: string[];
  data: number[];
}

interface SpeedingData {
  labels: string[];
  speeds: number[];
  colors: string[];
}

interface TripLocation {
  unique_id: number;
  from: string; // "(lat, lng) → Place"
  to: string;   // "(lat, lng) → Place"
}

// Helper function to parse coordinates from API
const parseCoordinates = (str: string): [number, number] => {
  const match = str.match(/\(([^)]+)\)/);
  if (!match) return [0, 0];
  const [lat, lng] = match[1].split(",").map(Number);
  return [lat, lng];
};

const MapComponent: React.FC<{ tripLocation: TripLocation | null }> = ({ tripLocation }) => {
  const defaultPosition: [number, number] = [19.123, 72.123]; // fallback

  if (!tripLocation) {
    return <p className="text-gray-500">Loading Trip Map…</p>;
  }

  const fromCoords = parseCoordinates(tripLocation.from);
  const toCoords = parseCoordinates(tripLocation.to);

  return (
    <MapContainer center={fromCoords} zoom={12} className="flex-1 rounded-2xl h-full">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      <Marker position={fromCoords}>
        <Popup>Start: {tripLocation.from.split("→")[1].trim()}</Popup>
      </Marker>
      <Marker position={toCoords}>
        <Popup>End: {tripLocation.to.split("→")[1].trim()}</Popup>
      </Marker>
      <Polyline positions={[fromCoords, toCoords]} color="blue" />
    </MapContainer>
  );
};

const New_Trips_Detailed: React.FC = () => {
  const { unique_id } = useParams<{ unique_id: string }>();
  const [tripInfo, setTripInfo] = useState<TripInfo | null>(null);
  const [tripLocation, setTripLocation] = useState<TripLocation | null>(null);
  const [drivingTrips, setDrivingTrips] = useState<DrivingTrips | null>(null);
  const [speedingData, setSpeedingData] = useState<SpeedingData | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch Trip Info
  useEffect(() => {
    if (!unique_id) return;

    const fetchTripInfo = async () => {
      try {
        const res = await fetch(`${baseURL}/trips/${unique_id}`);
        const data: TripInfo = await res.json();
        setTripInfo(data);
      } catch (err) {
        console.error("Error fetching trip info:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTripInfo();
  }, [unique_id]);

  // Fetch Trip Location
  useEffect(() => {
    if (!unique_id) return;

    const fetchTripLocation = async () => {
      try {
        const res = await fetch(`${baseURL}/trips/location/${unique_id}`);
        const data: TripLocation = await res.json();
        setTripLocation(data);
      } catch (err) {
        console.error("Error fetching trip location:", err);
      }
    };

    fetchTripLocation();
  }, [unique_id]);

  // Fetch Driving Trips
  useEffect(() => {
    const fetchDrivingTrips = async () => {
      try {
        const res = await fetch(`${baseURL}/driving_trips_daily`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filter_val: "last_1_month" }),
        });
        const data: DrivingTrips = await res.json();
        setDrivingTrips(data);
      } catch (err) {
        console.error("Error fetching driving trips:", err);
      }
    };
    fetchDrivingTrips();
  }, []);

  // Fetch Speeding Data
  useEffect(() => {
    const fetchSpeeding = async () => {
      try {
        const res = await fetch(`${baseURL}/speeding_analysis`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filter_val: "last_1_week" }),
        });
        const data: SpeedingData = await res.json();
        setSpeedingData(data);
      } catch (err) {
        console.error("Error fetching speeding analysis:", err);
      }
    };
    fetchSpeeding();
  }, []);

  return (
    <div className="p-6 lg:p-8 h-screen overflow-hidden bg-gray-200">
      <h2 className="text-lg font-semibold text-gray-800 mb-6">
        Trips Details –{" "}
        <span className="font-bold text-gray-900">
          {tripInfo?.unique_id || unique_id}
        </span>
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 auto-rows-fr h-[calc(100%-3rem)] bg-gray-200 ">

        {/* Trip Info */}
        <div className="bg-white rounded-2xl shadow-md h-[400px] p-6 flex flex-col justify-between">
          {loading ? (
            <p className="text-gray-500">Loading Trip Info…</p>
          ) : tripInfo ? (
            <>
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-full bg-[#EDEAFE] flex items-center justify-center text-[#5B4CAA] font-bold text-lg">
                  {tripInfo.name?.charAt(0)}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">{tripInfo.name}</h3>
                  <p className="text-sm text-gray-500">
                    Trip Id: <span className="font-medium">{tripInfo.unique_id}</span>
                  </p>
                </div>
              </div>

              <div className="flex gap-4 mt-6 flex-1">
                <div className="flex flex-col items-center">
                  <span className="w-3 h-3 rounded-full bg-[#6A56F1]" />
                  <div className="flex-1 border-l-3 border-dashed border-gray-300 my-2" />
                  <span className="w-3 h-3 rounded-full bg-[#6A56F1]" />
                </div>
                <div className="flex-1 flex flex-col justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{tripInfo.start_location}</p>
                    <p className="mt-1 text-sm font-semibold text-gray-800">
                      {new Date(tripInfo.start_time).toLocaleString()}
                    </p>
                  </div>
                  <div className="mt-6 sm:mt-8">
                    <p className="text-sm text-gray-600">{tripInfo.end_location}</p>
                    <p className="mt-1 text-sm font-semibold text-gray-800">
                      {new Date(tripInfo.end_time).toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <p className="text-gray-500">No trip data found.</p>
          )}
        </div>

        {/* Map */}
        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col h-[400px]">
          <MapComponent tripLocation={tripLocation} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Driving Trips Daily */}
        <div className="bg-white p-6 rounded-2xl h-[400px] shadow">
          <h2 className="font-semibold text-lg mb-4">Driving Trips Daily</h2>
          {drivingTrips ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={drivingTrips.labels.map((label, i) => ({
                  day: label,
                  trips: drivingTrips.data[i],
                }))}
                margin={{ top: 20, right: 20, left: 0, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="trips" fill="#8884d8" radius={[5, 5, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center">Loading Driving Trips…</p>
          )}
        </div>

        {/* Speeding Analysis */}
        <div className="bg-white p-6 rounded-2xl h-[400px] shadow">
          <h2 className="font-semibold text-lg mb-4">Speeding Analysis</h2>
          {speedingData ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={speedingData.labels.map((label, i) => ({
                  hour: label,
                  speed: speedingData.speeds[i],
                  color: speedingData.colors[i],
                }))}
                layout="vertical"
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="hour" type="category" />
                <Tooltip />
                <Bar dataKey="speed">
                  {speedingData.speeds.map((_, i) => (
                    <Cell key={`cell-${i}`} fill={speedingData.colors[i]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center">Loading Speeding Data…</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default New_Trips_Detailed;
