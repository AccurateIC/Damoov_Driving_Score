// src/pages/Trips/TripDetails.tsx
import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { tripsMockData } from "../../data/mockTrips";
import { MapPinned } from "lucide-react";
import TimelineChart from './TimelineChart';
import RadarChart from './RadarChart';
import SpeedChart from './SpeedChart';

const TripDetails = () => {
  const [searchParams] = useSearchParams();
  const userId = searchParams.get("user") || "";
  const [searchInput, setSearchInput] = useState(userId);
  const [filteredTrips, setFilteredTrips] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState("timeline");

  useEffect(() => {
    const filtered = tripsMockData.filter((t) => t.user === userId);
    setFilteredTrips(filtered);
  }, [userId]);

  return (
    <div className="flex min-h-screen bg-gray-50 p-6 gap-6">
      {/* Left: Trip List */}
      <div className="w-1/3 bg-white rounded shadow p-4 space-y-4 overflow-y-auto">
        <div className="flex items-center gap-2">
          <button className="bg-green-100 text-green-600 px-4 py-1 rounded font-medium border border-green-300">
            List of Trips
          </button>
          <button className="bg-gray-100 text-gray-700 px-4 py-1 rounded font-medium border">
            Trip Details
          </button>
        </div>

        <div className="flex gap-2 mt-2">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search by User ID"
            className="border px-3 py-1 rounded w-full text-sm"
          />
          <button
            onClick={() => {
              const filtered = tripsMockData.filter(
                (t) => t.user === searchInput
              );
              setFilteredTrips(filtered);
            }}
            className="text-green-600 text-sm underline"
          >
            Reset search
          </button>
        </div>

        {filteredTrips.length === 0 ? (
          <p className="text-sm text-gray-500 mt-6">
            No trips found for given ID
          </p>
        ) : (
          filteredTrips.map((trip, index) => (
            <div
              key={index}
              className="p-3 rounded border border-gray-200 space-y-1 text-sm"
            >
              <div className="flex justify-between items-center">
                <div className="text-green-600 font-medium">{trip.date}</div>
                <span
                  className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                    trip.score > 80
                      ? "bg-green-100 text-green-700"
                      : trip.score > 50
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {trip.score}
                </span>
              </div>
              <div className="text-gray-600">{trip.from}</div>
              <div className="text-gray-600">{trip.to}</div>
              <div className="text-gray-400 text-xs">{trip.id}</div>
            </div>
          ))
        )}
      </div>

      {/* Right: Map & Analytics */}
      <div className="flex-1 space-y-6">
        {/* Map */}
        <div className="h-96 w-full rounded shadow overflow-hidden">
          <iframe
            title="Trip Map"
            src="https://maps.google.com/maps?q=37.7749,-122.4194&z=14&output=embed"
            width="100%"
            height="100%"
            allowFullScreen
            loading="lazy"
            style={{ border: 0 }}
          ></iframe>
        </div>

        {/* Tabs */}
        <div className="bg-white shadow rounded">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab("timeline")}
              className={`px-4 py-2 text-sm ${
                activeTab === "timeline"
                  ? "border-b-2 border-green-600 text-green-600"
                  : "text-gray-600"
              }`}
            >
              Timeline
            </button>
            <button
              onClick={() => setActiveTab("analytics")}
              className={`px-4 py-2 text-sm ${
                activeTab === "analytics"
                  ? "border-b-2 border-green-600 text-green-600"
                  : "text-gray-600"
              }`}
            >
              Overall Analytics
            </button>
            <button
              onClick={() => setActiveTab("speed")}
              className={`px-4 py-2 text-sm ${
                activeTab === "speed"
                  ? "border-b-2 border-green-600 text-green-600"
                  : "text-gray-600"
              }`}
            >
              Speeding Analysis
            </button>
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
