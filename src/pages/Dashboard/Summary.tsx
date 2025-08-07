// src/pages/Dashboard/Summary.tsx

import React, { useState } from "react";
import Chart from "../../components/Chart";
import Table from "../../components/Table";
import OverviewChart from "../../components/OverviewChart";

const Summary = () => {
  const [activeTab, setActiveTab] = useState<"performance" | "safe" | "eco">(
    "performance"
  );

  const performanceData = [
    {
      metric: "New Drivers",
      value: "104",
      percentage: "-21.21%",
      absolute: "-28",
    },
    {
      metric: "Active Drivers",
      value: "338",
      percentage: "-1.17%",
      absolute: "-4",
    },
    {
      metric: "Trips Number",
      value: "15,840",
      percentage: "+4.92%",
      absolute: "+743",
    },
    {
      metric: "Mileage",
      value: "237,644",
      percentage: "+3.43%",
      absolute: "+7,875",
    },
    {
      metric: "Time of Driving",
      value: "304,406",
      percentage: "+1.98%",
      absolute: "+5,915",
    },
  ];

  const safeDrivingData = [
    {
      metric: "Safety Score",
      value: "78",
      percentage: "+0.02%",
      absolute: "0.01",
    },
    {
      metric: "Acceleration",
      value: "79",
      percentage: "+1.37%",
      absolute: "1.07",
    },
    { metric: "Braking", value: "79", percentage: "+0.52%", absolute: "0.41" },
    {
      metric: "Cornering",
      value: "91",
      percentage: "+0.59%",
      absolute: "0.54",
    },
    {
      metric: "Speeding",
      value: "80",
      percentage: "-1.25%",
      absolute: "-1.01",
    },
    {
      metric: "Phone Usage",
      value: "87",
      percentage: "-0.95%",
      absolute: "-0.44",
    },
  ];

  const ecoDrivingData = [
    {
      metric: "Eco Score",
      value: "75",
      percentage: "-1.22%",
      absolute: "-0.93",
    },
    { metric: "Brakes", value: "74", percentage: "-1.56%", absolute: "-1.17" },
    { metric: "Tyres", value: "94", percentage: "-0.35%", absolute: "-0.33" },
    { metric: "Fuel", value: "92", percentage: "-0.24%", absolute: "-0.22" },
    {
      metric: "Depreciation",
      value: "39",
      percentage: "-5.73%",
      absolute: "-2.40",
    },
  ];

  const summaryColumns = [
    { header: "Metric", accessor: "metric" },
    { header: "Value", accessor: "value" },
    { header: "Percentage Change", accessor: "percentage" },
    { header: "Absolute Change", accessor: "absolute" },
  ];

  const barChartData = {
    type: "bar" as const,
    title: "14 Days of Last 2 Weeks Daily Trend",
    labels: [
      "06/19",
      "06/20",
      "06/21",
      "06/22",
      "06/23",
      "06/24",
      "06/25",
      "06/26",
      "06/27",
      "06/28",
      "06/29",
      "06/30",
      "07/01",
      "07/02",
      "07/03",
    ],
    datasets: [
      {
        label: "Mileage",
        data: [
          15000, 14500, 14000, 13500, 16000, 17500, 15500, 14800, 15200, 14300,
          16000, 16500, 15800, 14700, 3000,
        ],
        backgroundColor: "rgba(59,130,246,0.8)",
      },
    ],
  };
  const distributionChart = {
    type: "bar" as const,
    title: "",
    labels: [
      "<45.0",
      "45–50",
      "50–55",
      "55–60",
      "60–65",
      "65–70",
      "70–75",
      "75–80",
      "80–85",
      "85–90",
      "90–95",
      "95–100",
    ],
    datasets: [
      {
        label: "Drivers",
        data: [2, 3, 5, 12, 23, 33, 44, 51, 46, 31, 33, 24],
        backgroundColor: [
          "#EF4444",
          "#EF4444",
          "#EF4444", // Aggressive
          "#F97316",
          "#F97316",
          "#F97316",
          "#F97316", // Moderate
          "#10B981",
          "#10B981",
          "#10B981",
          "#10B981",
          "#10B981", // Safe
        ],
      },
    ],
    options: {
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true },
        datalabels: {
          anchor: "end",
          align: "end",
          color: "#000",
          font: { weight: "bold" },
          formatter: (value: number) => value,
        },
      },
      scales: {
        x: { ticks: { color: "#333" }, grid: { display: false } },
        y: { ticks: { color: "#333" }, grid: { color: "#e5e7eb" } },
      },
    },
  };

  const radarChartData = {
    type: "radar" as const,
    title: "",
    labels: [
      "AccelerationScore",
      "BrakingScore",
      "CorneringScore",
      "PhoneUsageScore",
      "SpeedingScore",
    ],
    datasets: [
      {
        label: "Score",
        data: [85, 85, 85, 85, 85],
        backgroundColor: "rgba(59,130,246,0.3)",
        borderColor: "rgba(59,130,246,1)",
        pointBackgroundColor: "rgba(59,130,246,1)",
      },
    ],
  };

  const getCurrentTabData = () => {
    if (activeTab === "safe") return safeDrivingData;
    if (activeTab === "eco") return ecoDrivingData;
    return performanceData;
  };

  const topAggressiveDrivers = [
    { id: 1, token: "7422AAC4E9...", name: "", distance: "379", score: 41 },
    { id: 2, token: "4359B9036A...", name: "", distance: "95", score: 43 },
    { id: 3, token: "747389D3BE...", name: "", distance: "152", score: 49 },
    { id: 4, token: "D2B6C71C...", name: "", distance: "1,199", score: 50 },
    { id: 5, token: "68409ADB...", name: "", distance: "428", score: 51 },
    { id: 6, token: "82869798...", name: "", distance: "464", score: 51 },
    { id: 7, token: "40BE3192...", name: "", distance: "261", score: 52 },
    {
      id: 8,
      token: "8D104C4F...",
      name: "Fako Franklin",
      distance: "96",
      score: 53,
    },
    { id: 9, token: "ACC66DBD...", name: "", distance: "240", score: 54 },
    { id: 10, token: "A049542D...", name: "", distance: "1,194", score: 55 },
  ];

  const topSafeDrivers = [
    {
      id: 1,
      token: "D845E7E7...",
      name: "Martin Devore",
      distance: "71",
      score: 100,
    },
    { id: 2, token: "6FC720D4E...", name: "", distance: "467", score: 99 },
    { id: 3, token: "9FA04C9D...", name: "CO RSB", distance: "280", score: 97 },
    { id: 4, token: "45DCFDB...", name: "", distance: "115", score: 97 },
    { id: 5, token: "7C213750F...", name: "", distance: "102", score: 97 },
    {
      id: 6,
      token: "7445928B...",
      name: "Danny Ward",
      distance: "1,590",
      score: 97,
    },
    { id: 7, token: "8634A445...", name: "", distance: "903", score: 97 },
    {
      id: 8,
      token: "F9488EC...",
      name: "paul mckeever",
      distance: "772",
      score: 96,
    },
    { id: 9, token: "2E08D57D...", name: "", distance: "563", score: 96 },
    {
      id: 10,
      token: "531A3D3F...",
      name: "Gilda Borges",
      distance: "260",
      score: 95,
    },
  ];

  const driverTableColumns = [
    { header: "#", accessor: "id" },
    { header: "Driver token", accessor: "token" },
    { header: "Full Name", accessor: "name" },
    { header: "Distance", accessor: "distance" },
    { header: "Score", accessor: "score" },
  ];

  return (
    <div className="space-y-6">
      {/* Tabs */}
      <div className="flex space-x-6 border-b pb-2">
        {["performance", "safe", "eco"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            className={`text-sm font-medium capitalize pb-1 ${
              activeTab === tab
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-500"
            }`}
          >
            {tab === "performance"
              ? "Performance"
              : tab === "safe"
              ? "Safe Driving"
              : "Eco Driving"}
          </button>
        ))}
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Last 2 Weeks Summary</h3>
        <Table columns={summaryColumns} data={getCurrentTabData()} />
      </div>
      <div>
        <h4 className="text-lg font-semibold text-gray-700 mb-4">
          Performance Overview (Last 14 Days)
        </h4>

        <OverviewChart />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-md border border-gray-200 h-[550px] flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-semibold mb-4 text-gray-800 ">
              Driver Distribution
            </h3>
            <Chart {...distributionChart} />
            <div className="flex justify-center mt-4 space-x-6 text-sm font-medium">
              <span className="text-red-600">Aggressive</span>
              <span className="text-orange-500">Moderate</span>
              <span className="text-green-600">Safe</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md border border-gray-200 min-h-[500px] flex flex-col">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            Safety Parameters
          </h3>
          <Chart {...radarChartData} />
        </div>
      </div>
      {/* Driver Tables */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h3 className="text-md font-semibold mb-3">
            Top 10 Aggressive Drivers
          </h3>
          <Table columns={driverTableColumns} data={topAggressiveDrivers} />
        </div>
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h3 className="text-md font-semibold mb-3">Top 10 Safe Drivers</h3>
          <Table columns={driverTableColumns} data={topSafeDrivers} />
        </div>
      </div> 
    </div>
  );
};

export default Summary;
