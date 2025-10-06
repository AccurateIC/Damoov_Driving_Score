import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { tripsMockData } from "../../data/mockTrips";
import { MapPinned } from "lucide-react";
import TimelineChart from "./TimelineChart";
import RadarChart from "./RadarChart";
import SpeedChart from "./SpeedChart";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  Tooltip,
} from "react-leaflet";
import L from "leaflet";

const baseURL = import.meta.env.VITE_BASE_URL ;

const TripDetails = () => {
  // const [searchParams] = useSearchParams();
  // const userId = searchParams.get("user") || "";
  // const [searchInput, setSearchInput] = useState(userId);
  // const [filteredTrips, setFilteredTrips] = useState<any[]>([]);

  const markerIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });
  let fromCoords: [number, number] | null = null;
  let toCoords: [number, number] | null = null;

  const [activeTab, setActiveTab] = useState("timeline");
  const [tripDetails, setTripDetails] = useState([]);
  const [searchId, setSearchId] = useState("");
  // useEffect(() => {
  //   const filtered = tripsMockData.filter((t) => t.user === userId);
  //   setFilteredTrips(filtered);
  // }, [userId]);

  const handleSearch = () => {
   
    fetch(`${baseURL}/trips/location/${searchId}`)
      .then((response) => response.json())
      .then((data) => {
        setTripDetails(data);
      })
      .catch((error) => console.error("Error fetching trips:", error));
    console.log("tripDetails", tripDetails);
    // console.log("searchId djh", searchId);
  };

  if (tripDetails && tripDetails.from && tripDetails.to) {
    const fromParts = tripDetails.from
      .split("→")[0]
      .trim()
      .replace(/[()]/g, "")
      .split(",");
    const toParts = tripDetails.to
      .split("→")[0]
      .trim()
      .replace(/[()]/g, "")
      .split(",");

    fromCoords = [parseFloat(fromParts[0]), parseFloat(fromParts[1])];
    toCoords = [parseFloat(toParts[0]), parseFloat(toParts[1])];
  }
  const getAddress = (location: string) => location?.split("→")[1]?.trim() || "";
  const fromAddress = getAddress(tripDetails.from);
  const toAddress = getAddress(tripDetails.to);
  console.log(fromAddress);
  // const getCoords = (location: string) => {
  //   const coords = location
  //     .split("→")[0]
  //     .replace(/[()]/g, "")
  //     .trim()
  //     .split(",");
  //   return coords.map(Number) as [number, number];
  // };
  // const getAddress = (location: string) => location.split("→")[1].trim();

  // if (tripDetails?.from && tripDetails?.to) {
  //   const fromCoords = getCoords(tripDetails.from);
  //   const toCoords = getCoords(tripDetails.to);

  //   const fromAddress = getAddress(tripDetails.from);
  //   const toAddress = getAddress(tripDetails.to);

  //   console.log(fromCoords, toCoords, fromAddress, toAddress);
  // }

  return (
    <div className="flex min-h-screen bg-gray-50 p-6 gap-6">
      <div className="w-1/3 bg-white rounded shadow p-4 space-y-4 overflow-y-auto">
        <div className="flex items-center gap-2">
          {/* <button className="bg-green-100 text-green-600 px-4 py-1 rounded font-medium border border-green-300">
            List of Trips
          </button> */}
          <h1 className="bg-gray-100 font-bold text-gray-700 px-4 py-1 rounded  ">
            Trip Details
          </h1>
        </div>

        <div className="flex gap-2 mt-2">
          <input
            type="text"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            placeholder="Search by User ID"
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            className="border px-3 py-1 rounded w-full text-sm"
          />
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-4 py-2 rounded-md"
          >
            Search
          </button>

          {/* <button
            onClick={() => {
              const filtered = tripsMockData.filter(
                (t) => t.user === searchInput
              );
              setFilteredTrips(filtered);
            }}
            className="text-green-600 text-sm underline"
          >
            Reset 
          </button> */}
        </div>
        <div>
          {/* <div className="p-3 rounded border border-gray-200 space-y-2 text-sm">
  <div className="text-gray-800 font-semibold">Unique Id:  
    {tripDetails.unique_id}
  </div>
  <div>
    <span className="font-medium text-green-600">From:</span> {tripDetails.from}
  </div>
  <div>
    <span className="font-medium text-blue-600">To:</span> {tripDetails.to}
  </div>
</div> */}
          {tripDetails && Object.keys(tripDetails).length > 0 && (
            <div className="p-3 rounded border border-gray-200 space-y-1 text-sm">
              <div className="text-gray-800 font-semibold">
                Unique ID {tripDetails.unique_id}
              </div>
              <div className="flex items-start">
                <span className="font-medium text-green-600 mr-2">From</span>
                <span>{fromAddress}</span>
              </div>
              <div className="flex items-start">
                <span className="font-medium text-red-600 mr-2">To </span>
                <span>{toAddress}</span>
              </div>
            </div>
          )}
        </div>

        {/* 15610303 */}

        {/* {filteredTrips.length === 0 ? (
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
        )} */}
      </div>

      <div className="flex-1 space-y-6">
        {/* <div className="h-96 w-full rounded shadow overflow-hidden">
          <iframe
            title="Trip Map"
            src="https://maps.google.com/maps?q=37.7749,-122.4194&z=14&output=embed"
            width="100%"
            height="100%"
            allowFullScreen
            loading="lazy"
            style={{ border: 0 }}
          ></iframe>
        </div> */}
        <div className="h-96 w-full rounded shadow overflow-hidden">
          {fromCoords && toCoords ? (
            <MapContainer
              center={fromCoords}
              zoom={15}
              style={{ height: "100%", width: "100%" }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                // attribution="&copy; OpenStreetMap contributors"
              />

              <Marker position={fromCoords} icon={markerIcon}>
                <Tooltip sticky className="custom-tooltip-box">
                   {fromAddress}
                </Tooltip>
              </Marker>

              <Marker position={toCoords} icon={markerIcon}>
                <Tooltip sticky className="custom-tooltip-box">
                   {toAddress}
                </Tooltip>
              </Marker>
              <Polyline
                positions={[fromCoords, toCoords]}
                color="blue"
                weight={4}
              />
            </MapContainer>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Search for a trip to see markers
            </div>
          )}
        </div>

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
