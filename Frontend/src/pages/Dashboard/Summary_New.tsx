import React, { use, useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
// import OverviewChart from "../../components/OverviewChart";
import BarChartGraph from "../../components/BarchartGraph";
import TopDriversTable from "../../components/TopDrivers";
import Dashboard from "../../components/DriverDistribution";
import { Bell, User } from "lucide-react";

interface StatCard {
  label: string;
  value: string | number;
  period: string;
  trend: string;
  trendColor: string;
}

interface ChartData {
  name: string;
  value: number;
}

interface Driver {
  avg_score: number;
  device_id: string;
  name: string;
  total_distance: number;
}

interface TopDriversResponse {
  aggressive_drivers: Driver[];
  safe_drivers: Driver[];
}

const performanceData: ChartData[] = [
  { name: "Jan", value: 25 },
  { name: "Feb", value: 30 },
  { name: "Mar", value: 40 },
  { name: "Apr", value: 50 },
  { name: "May", value: 55 },
  { name: "Jun", value: 20 },
  { name: "Jul", value: 75 }, // Highlighted bar
  { name: "Aug", value: 60 },
  { name: "Sep", value: 62 },
  { name: "Oct", value: 45 },
  { name: "Nov", value: 33 },
  { name: "Dec", value: 28 },
];

const baseURL = import.meta.env.VITE_BASE_URL || "http://1270.0.1:5000";

const Summary: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"performance" | "safe" | "eco">(
    "performance"
  );

  const [selectedDays, setSelectedDays] = useState(14);

  const [top10Aggresive, setTop10Aggresive] = useState<Driver[]>([]);
  const [top10Safe, setTop10Safe] = useState<Driver[]>([]);

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

  const [performanceData, setPerformanceData] = useState<
    { metric: string; value: string }[]
  >([]);
  // useEffect(() => {
  //   const filterValue = getFilterValue(selectedDays);
  //   fetch(`${baseURL}/performance_summary?filter=${filterValue}`)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       // Build array dynamically only with API data:
  //       setPerformanceData([
  //         { metric: "New Drivers", value: data.new_drivers.toString() },
  //         { metric: "Active Drivers", value: data.active_drivers.toString() },
  //         { metric: "Trip Numbers", value: data.trips_number.toString() },
  //         { metric: "Mileage", value: data.mileage.toString() },
  //         { metric: "Time of Driving", value: data.time_of_driving.toString() },
  //       ]);
  //     })
  //     .catch((err) => console.error(err));
  // }, [selectedDays]);

  const fetchPerformanceSummary = async (filterValue: string) => {
    try {
      const res = await fetch(
        `${baseURL}/performance_summary?filter=${filterValue}`
      );
      if (!res.ok) throw new Error("Failed to fetch performance summary");
      const data = await res.json();
      return [
        { metric: "New Drivers", value: data.new_drivers.toString() },
        { metric: "Active Drivers", value: data.active_drivers.toString() },
        { metric: "Trip Numbers", value: data.trips_number.toString() },
        { metric: "Mileage", value: data.mileage.toString() },
        { metric: "Time of Driving", value: data.time_of_driving.toString() },
      ];
    } catch (err) {
      console.error("Error fetching performance data:", err);
      return []; // safe fallback
    }
  };

  const fetchSafeDrivingSummary = async (filter: string) => {
    const res = await fetch(`${baseURL}/safe_driving_summary?filter=${filter}`);
    if (!res.ok) throw new Error("Failed to fetch safe driving summary");
    const data = await res.json();

    // 🔹 Transform API response into UI-ready format here
    return [
      { metric: "Safety Score", value: data.safety_score.toString() },
      {
        metric: "Acceleration Score",
        value: data.acceleration_score.toString(),
      },
      { metric: "Braking Score", value: data.braking_score.toString() },
      { metric: "Cornering Score", value: data.cornering_score.toString() },
      { metric: "Speeding Score", value: data.speeding_score.toString() },
      { metric: "Phone Usage Score", value: data.phone_usage_score.toString() },
      { metric: "Trip Count", value: data.trip_count.toString() },
    ];
  };

  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);
    const load = async () => {
      const result = await fetchPerformanceSummary(filterValue);
      setPerformanceData(result);
    };

    fetchSafeDrivingSummary(filterValue)
      .then((safeData) => setSafeDrivingData(safeData))
      .catch((err) => console.error("Error fetching safe driving data:", err));

    fetchEcoDrivingSummary(filterValue)
      .then((ecoData) => setEcoDrivingData(ecoData))
      .catch((err) => console.error("Error fetching eco driving data:", err));

    load();

    fetchTopDrivers();
  }, [selectedDays]);

  const [safeDrivingData, setSafeDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  // useEffect(() => {
  //   console.log("selectedDays", selectedDays);
  //   const filterValue = getFilterValue(selectedDays);
  //   fetch(`${baseURL}/safe_driving_summary?filter=${filterValue}`)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setSafeDrivingData([
  //         { metric: "Safety Score", value: data.safety_score.toString() },
  //         {
  //           metric: "Acceleration Score",
  //           value: data.acceleration_score.toString(),
  //         },
  //         { metric: "Braking Score", value: data.braking_score.toString() },
  //         { metric: "Cornering Score", value: data.cornering_score.toString() },
  //         { metric: "Speeding Score", value: data.speeding_score.toString() },
  //         {
  //           metric: "Phone Usage Score",
  //           value: data.phone_usage_score.toString(),
  //         },
  //         { metric: "Trip Count", value: data.trip_count.toString() },
  //       ]);
  //     })
  //     .catch((err) => console.error("Error fetching safe driving data:", err));
  // }, [selectedDays]);

  const [ecoDrivingData, setEcoDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  const fetchTopDrivers = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/fetch_top_drivers");
      const data: TopDriversResponse = await res.json();

      setTop10Aggresive(data.aggressive_drivers);
      setTop10Safe(data.safe_drivers);
    } catch (error) {
      console.error("Failed to fetch top drivers:", error);
    }
  };

  // useEffect(() => {
  //   const filterValue = getFilterValue(selectedDays);

  //   fetch(`${baseURL}/eco_driving_summary?filter=${filterValue}`)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setEcoDrivingData([
  //         { metric: "Eco Score", value: data.eco_score.toString() },
  //         { metric: "Brakes Score", value: data.brakes_score.toString() },
  //         { metric: "Tyres Score", value: data.tires_score.toString() },
  //         { metric: "Fuel Score", value: data.fuel_score.toString() },
  //         { metric: "Trip Count", value: data.trip_count.toString() },
  //       ]);
  //     })

  //     .catch((err) => console.error("Error fetching eco driving data:", err));
  // }, [selectedDays]);
  const fetchEcoDrivingSummary = async (filter: string) => {
    try {
      const res = await fetch(
        `${baseURL}/eco_driving_summary?filter=${filter}`
      );
      if (!res.ok) throw new Error("Failed to fetch eco driving summary");

      const data = await res.json();

      // Transform into UI-ready format
      return [
        { metric: "Eco Score", value: data.eco_score.toString() },
        { metric: "Brakes Score", value: data.brakes_score.toString() },
        { metric: "Tyres Score", value: data.tires_score.toString() },
        { metric: "Fuel Score", value: data.fuel_score.toString() },
        { metric: "Trip Count", value: data.trip_count.toString() },
      ];
    } catch (err) {
      console.error("Error fetching eco driving data:", err);
      return [];
    }
  };

  const getCurrentTabData = () => {
    if (activeTab === "safe") return safeDrivingData;
    if (activeTab === "eco") return ecoDrivingData;
    return performanceData;
  };

  return (
    <div className="min-h-screen  px-4 pt-1  ">
      <div>
        {/* Breadcrumb */}
        <div
          className="  2xl:mx-[32px] xl:mx-[32px] 
       max-w-[1081px]  xl:max-w-[1200px] 2xl:max-w-[1830px]
       "
        >
          <p className="md:w-[204px]  md:h-[30px] font-medium text-gray-400 mb-[23px]">
            Dashboard &gt;{" "}
            <span className="font-bold text-xl  text-gray-800">Summary</span>
          </p>
        </div>
        {/* Tabs + Filter */}
        <div
          className="flex flex-col 
        // 2xl:max-h-[478px]
        //  max-w-[1080px]   xl:max-w-[1200px]  2xl:max-w-[1530px] 
        max-w-[1081px]  xl:max-w-[1200px] 2xl:max-w-[1830px] 2xl:mx-[32px] 
        gap-8  "
        >
          <div className=" flex  justify-between  ">
            <div className="flex md:gap-[32px] md:mx-[12px]   ">
              {["performance", "safe", "eco"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab as any)}
                  className={`text-[18px] font-semibold capitalize pb-2 transition-colors duration-200 ${
                    activeTab === tab
                      ? "text-blue-600 border-b-2 border-blue-600"
                      : "text-gray-500 hover:text-gray-700"
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
            {/* <select
              value={selectedDays}
              onChange={(e) => setSelectedDays(Number(e.target.value))}
              className="border shrink-0 md:w-[115px] md:h-[42px] 2xl:w-[145px] 2xl:h-[42px] bg-white  px-2 2xl:mx-[10px]   
              rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value={7}>Last 7 Days</option>
              <option value={14}>Last 14 Days</option>
              <option value={30}>Last 30 Days</option>
              <option value={60}>Last 60 Days</option>
            </select> */}
            <div className="relative">
              <select
                value={selectedDays}
                onChange={(e) => setSelectedDays(Number(e.target.value))}
                className="
      border 
      md:w-[115px] md:h-[42px] 2xl:w-[145px] 2xl:h-[42px]
      bg-white px-2 pr-8 2xl:mx-[1px]   
      rounded-md text-sm
       focus:outline-none
      appearance-none
    "
              >
                <option value={7}>Last 7 Days</option>
                <option value={14}>Last 14 Days</option>
                <option value={30}>Last 30 Days</option>
                <option value={60}>Last 60 Days</option>
              </select>

              {/* Custom dropdown arrow */}
              <div className="pointer-events-none absolute inset-y-0 right-2 flex items-center text-gray-500">
                ▼
              </div>
            </div>
          </div>
          {/* Stats Cards */}
          <div className="grid  grid-cols-1 sm:grid-cols-2  gap-4 md:grid-cols-5 2xl:grid-cols-6   mb-8">
            {getCurrentTabData().map((stat) => (
              <div
                key={stat.metric}
                className="flex flex-col bg-white mb-4 gap-4 2xl:max-w-[209px] 2xl:max-h-[192px] rounded-xl shadow-sm p-8  hover:shadow-md transition-shadow"
              >
                <p className="text-sm font-medium  text-gray-400  ">
                  {stat.metric}
                </p>
                <p className="text-4xl  font-bold text-gray-800">
                  {stat.value}
                </p>
                <p className=" font-normal text-sm -2 flex gap-3 ">
                  Last Month{" "}
                  <span className="font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl">
                    {" "}
                    25%
                  </span>
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Chart + Tables Section */}

        <div
          className="
       
       max-w-[1081px]  xl:max-w-[1200px] 2xl:max-w-[1830px] 2xl:mx-[32px] 
"
        >
          <div className=" text-base font-medium py-4">
            {" "}
            Performance Overview
          </div>
          <div className=" 2xl:max-h-[620px]  2xl:min-h-[430px]">
            <BarChartGraph selectedDays={selectedDays} />
          </div>

          <div className=" mt-[32px]">
            <Dashboard selectedDays={selectedDays} />
          </div>

          <div className=" mt-[32px]">
            <TopDriversTable
              title="Top 10 Aggresive Drivers"
              drivers={top10Aggresive}
            />
          </div>

          <div className=" mt-[32px]">
            <TopDriversTable title="Top 10 Safe Drivers" drivers={top10Safe} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Summary;
