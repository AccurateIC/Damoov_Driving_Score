import React, { use, useEffect, useState } from "react";
import Chart from "../../components/Chart";
import Table from "../../components/Table";
import OverviewChart from "../../components/OverviewChart";

const Summary = () => {
  const [activeTab, setActiveTab] = useState<"performance" | "safe" | "eco">(
    "performance"
  );

  const [performanceData, setPerformanceData] = useState<
    { metric: string; value: string }[]
  >([]);
  const [ecoDrivingData, setEcoDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  const [selectedDays, setSelectedDays] = useState(14);

  const getFilterValue = (days: number) => {
    switch (days) {
      case 7:
        return "last_1_week";
      case 14:
        return "last_2_weeks";
      case 30:
        return "last_1_month";
      case 60:
        return "last_2_months";
      default:
        return "last_2_weeks";
    }
  };

  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);
    console.log("filterValue", filterValue);
    fetch(`http://127.0.0.1:5000/performance_summary?filter=${filterValue}`)
      .then((res) => res.json())
      .then((data) => {
        setPerformanceData([
          { metric: "New Drivers", value: data.new_drivers.toString() },
          { metric: "Active Drivers", value: data.active_drivers.toString() },
          { metric: "Trips Number", value: data.trips_number.toString() },
          { metric: "Mileage", value: data.mileage.toString() },
          { metric: "Time of Driving", value: data.time_of_driving.toString() },
        ]);
      })
      .catch((err) => console.error("Error fetching performance data:", err));
  }, [selectedDays]);

  const [safeDrivingData, setSafeDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);
    console.log("filterValue", filterValue);
    fetch(`http://127.0.0.1:5000/safe_driving_summary?filter=${filterValue}`)
      .then((res) => res.json())
      .then((data) => {
        setSafeDrivingData([
          { metric: "Safety Score", value: data.safety_score.toString() },
          {
            metric: "Acceleration Score",
            value: data.acceleration_score.toString(),
          },
          { metric: "Braking Score", value: data.braking_score.toString() },
          { metric: "Cornering Score", value: data.cornering_score.toString() },
          { metric: "Speeding Score", value: data.speeding_score.toString() },
          {
            metric: "Phone Usage Score",
            value: data.phone_usage_score.toString(),
          },
          { metric: "Trip Count", value: data.trip_count.toString() },
        ]);
      })
      .catch((err) => console.error("Error fetching safe driving data:", err));
  }, [selectedDays]);

  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);

    fetch(`http://127.0.0.1:5000/eco_driving_summary?filter=${filterValue}`)
      .then((res) => res.json())
      .then((data) => {
        setEcoDrivingData([
          { metric: "Eco Score", value: data.eco_score.toString() },
          { metric: "Brakes Score", value: data.brakes_score.toString() },
          { metric: "Tyres Score", value: data.tires_score.toString() },
          { metric: "Fuel Score", value: data.fuel_score.toString() },
          { metric: "Trip Count", value: data.trip_count.toString() },
        ]);
      })

      .catch((err) => console.error("Error fetching eco driving data:", err));
  }, [selectedDays]);

  const summaryColumns = [
    { header: "Metric", accessor: "metric" },
    { header: "Value", accessor: "value" },
  ];
  const [distributionChart, setDistributionChart] = useState<any>(null);

  const [safeScore, setSafeScore] = useState([]);
  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);

    fetch("http://127.0.0.1:5000/driver_distribution", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filter_val: filterValue,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSafeScore(data);
        console.log("safe Score:", safeScore[0]);
        console.log("Driver Distribution Data:", data);
        setDistributionChart({
          type: "bar" as const,
          title: "",
          labels: data.labels,
          datasets: [
            {
              label: "Drivers",
              data: data.data,
              backgroundColor: data.labels.map((_: string, idx: number) => {
                if (idx < 3) return "#10B981"; // red
                if (idx < 7) return "#F97316"; // orange
                return "#10B981"; // green
              }),
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
        });
      })
      .catch((err) => {
        console.error("Error fetching driver distribution data:", err);
      });
  }, [selectedDays]);

  // const [radarChartData, serRadarChartData] = useState<any>(null);
  // http://127.0.0.1:5000/safety_params

  const [radarChartData, setRadarChartData] = useState<any>(null);

  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);

    fetch("http://127.0.0.1:5000/safety_params", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filter_val: filterValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Safety Params Data:", data);

        setRadarChartData({
          type: "radar" as const,
          title: "Safety Parameters",
          labels: data.labels, // dynamic labels
          datasets: [
            {
              label: "Score",
              data: data.data, // dynamic values
              backgroundColor: "rgba(59,130,246,0.3)",
              borderColor: "rgba(59,130,246,1)",
              pointBackgroundColor: "rgba(59,130,246,1)",
            },
          ],
        });
      })
      .catch((err) => {
        console.error("Error fetching safety params data:", err);
      });
  }, [selectedDays]);

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
      <div>
        <select
          value={selectedDays}
          onChange={(e) => setSelectedDays(Number(e.target.value))}
          className="border border-green-600 text-green-600 px-4 py-2 rounded-md text-sm"
        >
          <option value={7}>Last 7 Days</option>
          <option value={14}>Last 14 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={60}>Last 60 Days</option>
        </select>
      </div>
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
        {/* <h3 className="text-lg font-semibold mb-2">Last 2 Weeks Summary</h3> */}
        <Table columns={summaryColumns} data={getCurrentTabData()} />
      </div>
      <div>
        <h4 className="text-lg font-semibold text-gray-700 mb-4">
          Performance Overview (Last 14 Days)
        </h4>
        <OverviewChart selectedDays={selectedDays} />
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
