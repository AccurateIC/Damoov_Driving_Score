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