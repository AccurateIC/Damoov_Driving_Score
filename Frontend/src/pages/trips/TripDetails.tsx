// import React, { useEffect, useState } from "react";
// import { useSearchParams } from "react-router-dom";
// import { tripsMockData } from "../../data/mockTrips";
// import { MapPinned } from "lucide-react";
// import TimelineChart from "./TimelineChart";
// import RadarChart from "./RadarChart";
// import SpeedChart from "./SpeedChart";
// import {
//   MapContainer,
//   TileLayer,
//   Marker,
//   Popup,
//   Polyline,
//   Tooltip,
// } from "react-leaflet";
// import L from "leaflet";

// const TripDetails = () => {
//   // const [searchParams] = useSearchParams();
//   // const userId = searchParams.get("user") || "";
//   // const [searchInput, setSearchInput] = useState(userId);
//   // const [filteredTrips, setFilteredTrips] = useState<any[]>([]);

//   const markerIcon = new L.Icon({
//     iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
//     iconSize: [25, 41],
//     iconAnchor: [12, 41],
//   });
//   let fromCoords: [number, number] | null = null;
//   let toCoords: [number, number] | null = null;

//   const [activeTab, setActiveTab] = useState("timeline");
//   const [tripDetails, setTripDetails] = useState([]);
//   const [searchId, setSearchId] = useState("");
//   // useEffect(() => {
//   //   const filtered = tripsMockData.filter((t) => t.user === userId);
//   //   setFilteredTrips(filtered);
//   // }, [userId]);

//   const handleSearch = () => {
//     // Load trips on component mount
//     // http://127.0.0.1:5000/trips/location/15610303
//     fetch(`http://127.0.0.1:5000/trips/location/${searchId}`)
//       .then((response) => response.json())
//       .then((data) => {
//         setTripDetails(data);
//       })
//       .catch((error) => console.error("Error fetching trips:", error));
//     console.log("tripDetails", tripDetails);
//     // console.log("searchId djh", searchId);
//   };

//   if (tripDetails && tripDetails.from && tripDetails.to) {
//     const fromParts = tripDetails.from
//       .split("→")[0]
//       .trim()
//       .replace(/[()]/g, "")
//       .split(",");
//     const toParts = tripDetails.to
//       .split("→")[0]
//       .trim()
//       .replace(/[()]/g, "")
//       .split(",");

//     fromCoords = [parseFloat(fromParts[0]), parseFloat(fromParts[1])];
//     toCoords = [parseFloat(toParts[0]), parseFloat(toParts[1])];
//   }
//   const getAddress = (location: string) => location?.split("→")[1]?.trim() || "";
//   const fromAddress = getAddress(tripDetails.from);
//   const toAddress = getAddress(tripDetails.to);
//   console.log(fromAddress);
//   // const getCoords = (location: string) => {
//   //   const coords = location
//   //     .split("→")[0]
//   //     .replace(/[()]/g, "")
//   //     .trim()
//   //     .split(",");
//   //   return coords.map(Number) as [number, number];
//   // };
//   // const getAddress = (location: string) => location.split("→")[1].trim();

//   // if (tripDetails?.from && tripDetails?.to) {
//   //   const fromCoords = getCoords(tripDetails.from);
//   //   const toCoords = getCoords(tripDetails.to);

//   //   const fromAddress = getAddress(tripDetails.from);
//   //   const toAddress = getAddress(tripDetails.to);

//   //   console.log(fromCoords, toCoords, fromAddress, toAddress);
//   // }

//   return (
//     <div className="flex min-h-screen bg-gray-50 p-6 gap-6">
//       <div className="w-1/3 bg-white rounded shadow p-4 space-y-4 overflow-y-auto">
//         <div className="flex items-center gap-2">
//           {/* <button className="bg-green-100 text-green-600 px-4 py-1 rounded font-medium border border-green-300">
//             List of Trips
//           </button> */}
//           <h1 className="bg-gray-100 font-bold text-gray-700 px-4 py-1 rounded  ">
//             Trip Details
//           </h1>
//         </div>

//         <div className="flex gap-2 mt-2">
//           <input
//             type="text"
//             value={searchId}
//             onChange={(e) => setSearchId(e.target.value)}
//             placeholder="Search by User ID"
//             onKeyDown={(e) => e.key === "Enter" && handleSearch()}
//             className="border px-3 py-1 rounded w-full text-sm"
//           />
//           <button
//             onClick={handleSearch}
//             className="bg-blue-600 text-white px-4 py-2 rounded-md"
//           >
//             Search
//           </button>

//           {/* <button
//             onClick={() => {
//               const filtered = tripsMockData.filter(
//                 (t) => t.user === searchInput
//               );
//               setFilteredTrips(filtered);
//             }}
//             className="text-green-600 text-sm underline"
//           >
//             Reset
//           </button> */}
//         </div>
//         <div>
//           {/* <div className="p-3 rounded border border-gray-200 space-y-2 text-sm">
//   <div className="text-gray-800 font-semibold">Unique Id:
//     {tripDetails.unique_id}
//   </div>
//   <div>
//     <span className="font-medium text-green-600">From:</span> {tripDetails.from}
//   </div>
//   <div>
//     <span className="font-medium text-blue-600">To:</span> {tripDetails.to}
//   </div>
// </div> */}
//           {tripDetails && Object.keys(tripDetails).length > 0 && (
//             <div className="p-3 rounded border border-gray-200 space-y-1 text-sm">
//               <div className="text-gray-800 font-semibold">
//                 Unique ID {tripDetails.unique_id}
//               </div>
//               <div className="flex items-start">
//                 <span className="font-medium text-green-600 mr-2">From</span>
//                 <span>{fromAddress}</span>
//               </div>
//               <div className="flex items-start">
//                 <span className="font-medium text-red-600 mr-2">To </span>
//                 <span>{toAddress}</span>
//               </div>
//             </div>
//           )}
//         </div>

//         {/* 15610303 */}

//         {/* {filteredTrips.length === 0 ? (
//           <p className="text-sm text-gray-500 mt-6">
//             No trips found for given ID
//           </p>
//         ) : (
//           filteredTrips.map((trip, index) => (
//             <div
//               key={index}
//               className="p-3 rounded border border-gray-200 space-y-1 text-sm"
//             >
//               <div className="flex justify-between items-center">
//                 <div className="text-green-600 font-medium">{trip.date}</div>
//                 <span
//                   className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
//                     trip.score > 80
//                       ? "bg-green-100 text-green-700"
//                       : trip.score > 50
//                       ? "bg-yellow-100 text-yellow-700"
//                       : "bg-red-100 text-red-700"
//                   }`}
//                 >
//                   {trip.score}
//                 </span>
//               </div>
//               <div className="text-gray-600">{trip.from}</div>
//               <div className="text-gray-600">{trip.to}</div>
//               <div className="text-gray-400 text-xs">{trip.id}</div>
//             </div>
//           ))
//         )} */}
//       </div>

//       <div className="flex-1 space-y-6">
//         {/* <div className="h-96 w-full rounded shadow overflow-hidden">
//           <iframe
//             title="Trip Map"
//             src="https://maps.google.com/maps?q=37.7749,-122.4194&z=14&output=embed"
//             width="100%"
//             height="100%"
//             allowFullScreen
//             loading="lazy"
//             style={{ border: 0 }}
//           ></iframe>
//         </div> */}
//         <div className="h-96 w-full rounded shadow overflow-hidden">
//           {fromCoords && toCoords ? (
//             <MapContainer
//               center={fromCoords}
//               zoom={15}
//               style={{ height: "100%", width: "100%" }}
//             >
//               <TileLayer
//                 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//                 // attribution="&copy; OpenStreetMap contributors"
//               />

//               <Marker position={fromCoords} icon={markerIcon}>
//                 <Tooltip sticky className="custom-tooltip-box">
//                    {fromAddress}
//                 </Tooltip>
//               </Marker>

//               <Marker position={toCoords} icon={markerIcon}>
//                 <Tooltip sticky className="custom-tooltip-box">
//                    {toAddress}
//                 </Tooltip>
//               </Marker>
//               <Polyline
//                 positions={[fromCoords, toCoords]}
//                 color="blue"
//                 weight={4}
//               />
//             </MapContainer>
//           ) : (
//             <div className="flex items-center justify-center h-full text-gray-500">
//               Search for a trip to see markers
//             </div>
//           )}
//         </div>

//         <div className="bg-white shadow rounded">
//           <div className="flex border-b">
//             <button
//               onClick={() => setActiveTab("timeline")}
//               className={`px-4 py-2 text-sm ${
//                 activeTab === "timeline"
//                   ? "border-b-2 border-green-600 text-green-600"
//                   : "text-gray-600"
//               }`}
//             >
//               Timeline
//             </button>
//             <button
//               onClick={() => setActiveTab("analytics")}
//               className={`px-4 py-2 text-sm ${
//                 activeTab === "analytics"
//                   ? "border-b-2 border-green-600 text-green-600"
//                   : "text-gray-600"
//               }`}
//             >
//               Overall Analytics
//             </button>
//             <button
//               onClick={() => setActiveTab("speed")}
//               className={`px-4 py-2 text-sm ${
//                 activeTab === "speed"
//                   ? "border-b-2 border-green-600 text-green-600"
//                   : "text-gray-600"
//               }`}
//             >
//               Speeding Analysis
//             </button>
//           </div>

//           <div className="p-4">
//             {activeTab === "timeline" && <TimelineChart />}
//             {activeTab === "analytics" && <RadarChart />}
//             {activeTab === "speed" && <SpeedChart />}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default TripDetails;

import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";
import { MapContainer, TileLayer, Polygon, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const polygonCoords: [number, number][] = [
  [18.559, 73.789],
  [18.563, 73.801],
  [18.552, 73.808],
  [18.545, 73.793],
];

const radarData = [
  { subject: "Acceleration", A: 85 },
  { subject: "Phone Usage", A: 70 },
  { subject: "Speeding", A: 60 },
  { subject: "Cornering", A: 75 },
  { subject: "Braking", A: 90 },
  { subject: "Handling", A: 80 },
];

const barData = [
  { time: "10:30", speed: "20", value: 2 },
  { time: "10:30", speed: "40", value: 5 },
  { time: "11:30", speed: "60", value: 3 },
  { time: "12:30", speed: "80", value: 6 },
  { time: "13:30", speed: "100+", value: 4 },
  { time: "14:30", speed: "50", value: 7 },
  { time: "15:30", speed: "30", value: 5 },
];

const BAR_COLORS = [
  "#8884d8",
  "#82ca9d",
  "#ffc658",
  "#ff7f50",
  "#00C49F",
  "#FF8042",
];

function FitBounds({ coords }: { coords: [number, number][] }) {
  const map = useMap();
  useEffect(() => {
    if (coords.length > 0) {
      map.fitBounds(coords as any, { padding: [40, 40] });
    }
  }, [map, coords]);
  return null;
}

const TripDetails: React.FC = () => {
  const { deviceId } = useParams<{ deviceId?: string }>();

  const tripInfo = {
    name: "Atharva D",
    tripId: deviceId ?? "77007700770077",
    startAddress: "Bhujbal Chowk, Mahalunge, Mulshi, Pune, Maharashtra, 411057",
    endAddress:
      "Hirai Sital Mandir, Sakhare Vasti, Hinjawadi, Pune, Maharashtra, 411057",
    startTime: "10.30 am",
    endTime: "5.30 pm",
    efficiency: 90,
  };

  return (
    <div className="p-6 lg:p-8 h-screen overflow-hidden">
      <h2 className="text-lg font-semibold text-gray-800 mb-6">
        Trips Details –{" "}
        <span className="font-bold text-gray-900">{tripInfo.tripId}</span>
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 auto-rows-fr h-[calc(100%-3rem)]">

        {/* Trip Info */}
        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col justify-between h-full">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-full bg-[#EDEAFE] flex items-center justify-center text-[#5B4CAA] font-bold text-lg">
              {tripInfo.name.charAt(0)}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">
                {tripInfo.name}
              </h3>
              <p className="text-sm text-gray-500">
                Trip Id: <span className="font-medium">{tripInfo.tripId}</span>
              </p>
            </div>
          </div>

          <div className="flex gap-4 mt-6 flex-1">
            <div className="flex flex-col items-center">
              <span className="w-3 h-3 rounded-full bg-[#6A56F1]" />
              <div className="flex-1 border-l-2 border-dashed border-gray-300 my-2" />
              <span className="w-3 h-3 rounded-full bg-[#6A56F1]" />
            </div>
            <div className="flex-1 flex flex-col justify-between">
              <div>
                <p className="text-sm text-gray-600">{tripInfo.startAddress}</p>
                <p className="mt-1 text-sm font-semibold text-gray-800">
                  {tripInfo.startTime}
                </p>
              </div>
              <div className="mt-6 sm:mt-8">
                <p className="text-sm text-gray-600">{tripInfo.endAddress}</p>
                <p className="mt-1 text-sm font-semibold text-gray-800">
                  {tripInfo.endTime}
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
              Travelled safer than other drivers with{" "}
              <span className="font-bold text-[#5B4CAA]">
                {tripInfo.efficiency}%
              </span>{" "}
              efficiency
            </p>
          </div>
        </div>

        {/* Map */}
        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col">
          <div className="flex-1 rounded-lg overflow-hidden">
            <MapContainer
              center={[18.56, 73.79]}
              zoom={13}
              scrollWheelZoom={false}
              className="w-full h-full"
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              <FitBounds coords={polygonCoords} />
              <Polygon
                positions={polygonCoords}
                pathOptions={{
                  color: "#5B4CAA",
                  fillColor: "#E8E4FB",
                  fillOpacity: 0.6,
                  weight: 2,
                }}
              />
            </MapContainer>
          </div>
        </div>

        {/* Driving Trips Daily */}
        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col">
          <h3 className="text-base font-semibold text-gray-700 mb-4">
            Driving Trips Daily
          </h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} />
                <Radar
                  dataKey="A"
                  stroke="#6A56F1"
                  fill="#6A56F1"
                  fillOpacity={0.6}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-4 mt-4 text-sm text-gray-600">
            {radarData.map((r) => (
              <div key={r.subject} className="w-full">
                <div className="flex items-center gap-1">
                  <span className="font-semibold text-[#333]">{r.A}</span>
                  <span className="text-xs text-gray-500">{r.subject}</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full mt-1">
                  <div
                    className="h-2 bg-blue-800 rounded-full"
                    style={{ width: `${r.A}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Speeding Analysis */}
        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col">
          <h3 className="text-base font-semibold text-gray-700 mb-4">
            Speeding Analysis
          </h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={barData}
                layout="vertical"
                margin={{ top: 20, right: 20, left: 10, bottom: 20 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis
                  dataKey="speed"
                  type="category"
                  tick={{ fontSize: 12 }}
                  width={60}
                />
                <Tooltip />
                <Bar dataKey="value" barSize={32} radius={[6, 6, 6, 6]}>
                  {barData.map((_, idx) => (
                    <Cell
                      key={idx}
                      fill={BAR_COLORS[idx % BAR_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripDetails;
