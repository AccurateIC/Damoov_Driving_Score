import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const chartLabels = Array.from({ length: 14 }, (_, i) => {
  const date = new Date();
  date.setDate(date.getDate() - (13 - i));
  return date.toISOString().split("T")[0]; 
});

const performanceTableData = [
  {
    date: "2025-07-22",
    newDrivers: 0,
    activeDrivers: 65,
    avgSpeed: 46,
    tripCount: 139,
    drivingTime: 3006,
    mileage: 2740,
    phoneUsageMin: 53,
    phoneUsageKm: 44,
    speedingKm: 295,
    nightDrivingMin: 344,
  },
  {
    date: "2025-07-21",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
  {
    date: "2025-07-20",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
  {
    date: "2025-07-19",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
  {
    date: "2025-07-18",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
  {
    date: "2025-07-17",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
  {
    date: "2025-07-16",
    newDrivers: 4,
    activeDrivers: 230,
    avgSpeed: 43,
    tripCount: 1113,
    drivingTime: 21009,
    mileage: 16266,
    phoneUsageMin: 537,
    phoneUsageKm: 388,
    speedingKm: 1524,
    nightDrivingMin: 1292,
  },
];

const safeDrivingTableData = [
  {
    date: "2025-07-22",
    safetyScore: 77,
    accelScore: 80,
    accelCount: 45,
    brakingScore: 81,
    brakingCount: 49,
    corneringScore: 92,
    corneringCount: 21,
    speedingScore: 75,
    speedingKm: 295,
    phoneScore: 86,
  },
  {
    date: "2025-07-21",
    safetyScore: 77,
    accelScore: 80,
    accelCount: 688,
    brakingScore: 81,
    brakingCount: 838,
    corneringScore: 92,
    corneringCount: 221,
    speedingScore: 75,
    speedingKm: 1524,
    phoneScore: 86,
  },
];
const chartDataSets = {
  Mileage: {
    labels: chartLabels,
    datasets: [
      {
        label: "Mileage",
        data: [2740, 16266, 17578, 18741, 18207, 17502, 19168, 16000, 15000, 18000, 17000, 16500, 15500, 14500],
        backgroundColor: "#4f46e5",
        borderRadius: 6,
      },
    ],
  },
  "Driving Time": {
    labels: chartLabels,
    datasets: [
      {
        label: "Driving Time",
        data: [3006, 21009, 19015, 23101, 22586, 22953, 24012, 22000, 21000, 23000, 22000, 21500, 22500, 23500],
        backgroundColor: "#16a34a",
        borderRadius: 6,
      },
    ],
  },
};

const OverviewChart = () => {
  const [selectedParam, setSelectedParam] = useState("Mileage");
  const [viewMode, setViewMode] = useState<"table" | "chart">("chart");
  const [activeTab, setActiveTab] = useState<"performance" | "safeDriving">(
    "performance"
  );

  return (
    <div className="bg-white shadow rounded-xl p-6 w-[70rem]">
      {/* <div className="mb-4 border-b border-gray-200">
        <nav className="flex space-x-4">
          <button
            className={`pb-2 px-4 font-medium ${
              activeTab === "performance"
                ? "border-b-2 border-blue-600 text-blue-600"
                : "text-gray-600"
            }`}
            onClick={() => setActiveTab("performance")}
          >
            Performance
          </button>
          <button
            className={`pb-2 px-4 font-medium ${
              activeTab === "safeDriving"
                ? "border-b-2 border-blue-600 text-blue-600"
                : "text-gray-600"
            }`}
            onClick={() => setActiveTab("safeDriving")}
          >
            Safe driving
          </button>
        </nav>
      </div> */}

      <div className="flex justify-between items-center mb-4">
        <div>
          <select
            onChange={(e) => setSelectedParam(e.target.value)}
            value={selectedParam}
            className="border border-gray-400 rounded px-4 py-2 font-semibold text-gray-700"
          >
            {Object.keys(chartDataSets).map((param) => (
              <option key={param} value={param}>
                {param}
              </option>
            ))}
          </select>
        </div>

        <div className="space-x-2">
          <button
            onClick={() => setViewMode("chart")}
            className={`px-4 py-2 text-sm rounded ${
              viewMode === "chart"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700"
            }`}
          >
            Chart
          </button>
          <button
            onClick={() => setViewMode("table")}
            className={`px-4 py-2 text-sm rounded ${
              viewMode === "table"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700"
            }`}
          >
            Table
          </button>
        </div>
      </div>

      {viewMode === "chart" && (
        <Bar data={chartDataSets[selectedParam]} options={{ responsive: true }} />
      )}

      {viewMode === "table" && (
        <div className="overflow-x-auto mt-4">
          {activeTab === "performance" ? (
            <table className="w-full text-sm border border-gray-200 rounded-lg">
              <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                  <th className="px-3 py-2">Date</th>
                  <th className="px-3 py-2">New drivers</th>
                  <th className="px-3 py-2">Active drivers</th>
                  <th className="px-3 py-2">Average speed</th>
                  <th className="px-3 py-2">Trips count</th>
                  <th className="px-3 py-2">Driving time, min</th>
                  <th className="px-3 py-2">Mileage, km</th>
                  <th className="px-3 py-2">Phone usage, min</th>
                  <th className="px-3 py-2">Phone usage, km</th>
                  <th className="px-3 py-2">Speeding, km</th>
                  <th className="px-3 py-2">Night driving, min</th>
                </tr>
              </thead>
              <tbody>
                {performanceTableData.map((row, i) => (
                  <tr key={i} className={i % 2 ? "bg-gray-50" : "bg-white"}>
                    <td className="px-3 py-2">{row.date}</td>
                    <td className="px-3 py-2">{row.newDrivers}</td>
                    <td className="px-3 py-2">{row.activeDrivers}</td>
                    <td className="px-3 py-2">{row.avgSpeed}</td>
                    <td className="px-3 py-2">{row.tripCount}</td>
                    <td className="px-3 py-2">{row.drivingTime}</td>
                    <td className="px-3 py-2">{row.mileage}</td>
                    <td className="px-3 py-2">{row.phoneUsageMin}</td>
                    <td className="px-3 py-2">{row.phoneUsageKm}</td>
                    <td className="px-3 py-2">{row.speedingKm}</td>
                    <td className="px-3 py-2">{row.nightDrivingMin}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <table className="w-full text-sm border border-gray-200 rounded-lg">
              <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                  <th className="px-3 py-2">Date</th>
                  <th className="px-3 py-2">Safety score</th>
                  <th className="px-3 py-2">Acceleration score</th>
                  <th className="px-3 py-2">Acceleration count</th>
                  <th className="px-3 py-2">Braking score</th>
                  <th className="px-3 py-2">Braking count</th>
                  <th className="px-3 py-2">Cornering score</th>
                  <th className="px-3 py-2">Cornering count</th>
                  <th className="px-3 py-2">Speeding score</th>
                  <th className="px-3 py-2">Speeding km</th>
                  <th className="px-3 py-2">Phone usage score</th>
                </tr>
              </thead>
              <tbody>
                {safeDrivingTableData.map((row, i) => (
                  <tr key={i} className={i % 2 ? "bg-gray-50" : "bg-white"}>
                    <td className="px-3 py-2">{row.date}</td>
                    <td className="px-3 py-2">{row.safetyScore}</td>
                    <td className="px-3 py-2">{row.accelScore}</td>
                    <td className="px-3 py-2">{row.accelCount}</td>
                    <td className="px-3 py-2">{row.brakingScore}</td>
                    <td className="px-3 py-2">{row.brakingCount}</td>
                    <td className="px-3 py-2">{row.corneringScore}</td>
                    <td className="px-3 py-2">{row.corneringCount}</td>
                    <td className="px-3 py-2">{row.speedingScore}</td>
                    <td className="px-3 py-2">{row.speedingKm}</td>
                    <td className="px-3 py-2">{row.phoneScore}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default OverviewChart;
