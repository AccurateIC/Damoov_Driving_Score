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

const Summary: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"performance" | "safe" | "eco">(
    "performance"
  );
  const [selectedDays, setSelectedDays] = useState(14);
  const [top10Aggresive, setTop10Aggresive] = useState<string>(
    "Top 10 Aggresive Drivers"
  );
  const [top10Safe, setTop10Safe] = useState<string>("Top 10 Safe Drivers");
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
  useEffect(() => {
    const filterValue = getFilterValue(selectedDays);
    fetch(`http://127.0.0.1:5000/performance_summary?filter=${filterValue}`)
      .then((res) => res.json())
      .then((data) => {
        // Build array dynamically only with API data:
        setPerformanceData([
          { metric: "New Drivers", value: data.new_drivers.toString() },
          { metric: "Active Drivers", value: data.active_drivers.toString() },
          { metric: "Trip Numbers", value: data.trips_number.toString() },
          { metric: "Mileage", value: data.mileage.toString() },
          { metric: "Time of Driving", value: data.time_of_driving.toString() },
        ]);
      })
      .catch((err) => console.error(err));
  }, [selectedDays]);

  const [safeDrivingData, setSafeDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  useEffect(() => {
    console.log("selectedDays", selectedDays);
    const filterValue = getFilterValue(selectedDays);
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

  const [ecoDrivingData, setEcoDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

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

  const getCurrentTabData = () => {
    if (activeTab === "safe") return safeDrivingData;
    if (activeTab === "eco") return ecoDrivingData;
    return performanceData;
  };

  //   <div className="bg-gray-50 min-h-screen py-8 px-4 md:px-12 font-inter">
  //     {/* Header */}
  //     <div className="flex items-center justify-between mb-2">
  //       <div>
  //         <div className="text-xs text-gray-400 mb-1">Good Morning,</div>
  //         <div className="text-lg font-semibold text-gray-800">Atharva D</div>
  //       </div>
  //       <div className="w-10 h-10 rounded-full bg-violet-200 flex items-center justify-center">
  //         <span role="img" aria-label="avatar">
  //           🧑‍💼
  //         </span>
  //       </div>
  //     </div>
  //     <div className="mb-2 text-xs text-gray-400">
  //       Dashboard &gt;{" "}
  //       <span className="font-semibold text-gray-800">Summary</span>
  //     </div>

  //     {/* Tabs */}
  //     <div className="flex gap-8 mb-8 border-b border-gray-200">

  //       {["performance", "safe", "eco"].map((tab) => (
  //         <button
  //           key={tab}
  //           onClick={() => setActiveTab(tab as any)}
  //           className={`text-sm font-semibold capitalize pb-2 ${
  //             activeTab === tab
  //               ? "text-blue-600 border-b-4 border-blue-600"
  //               : "text-gray-500 hover:text-gray-700"
  //           } transition-colors duration-200`}
  //         >
  //           {tab === "performance"
  //             ? "Performance"
  //             : tab === "safe"
  //             ? "Safe Driving"
  //             : "Eco Driving"}
  //         </button>
  //       ))}
  //       <div>
  //       <select
  //         value={selectedDays}
  //         onChange={(e) => setSelectedDays(Number(e.target.value))}
  //         className="border border-green-600 text-green-600 px-4 py-2 rounded-md text-sm"
  //       >
  //         <option value={7}>Last 7 Days</option>
  //         <option value={14}>Last 14 Days</option>
  //         <option value={30}>Last 30 Days</option>
  //         <option value={60}>Last 60 Days</option>
  //       </select>
  //     </div>
  //     </div>

  //     {/* Stats Cards */}
  //     <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 mb-8">
  //       {getCurrentTabData().map((stat) => (
  //         <div
  //           key={stat.metric}
  //           className="bg-white rounded-xl shadow-sm px-6 py-5"
  //         >
  //           <div className="text-sm text-gray-400">{stat.metric}</div>
  //           <div className="text-2xl font-bold text-gray-800">{stat.value}</div>

  //           {/* Optional period and trend */}
  //         </div>
  //       ))}
  //     </div>

  //     {/* Chart Card */}

  //       <div className=" w-full">
  //      <BarChartGraph selectedDays={selectedDays}/>
  //       {/* <OverviewChart  /> */}
  //       <Dashboard selectedDays={selectedDays}/>
  //       <TopDriversTable/>
  //     </div>
  //   </div>
  // );

  return (
    <div className="min-h-screen py-6 px-4 md:px-10 font-inter">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 w-[79vw]  border-rounded-lg  rounded-full bg-white shadow-sm p-4  ">
        <div>
          <p className="text-xs  text-gray-500  mb-1">Good Morning,</p>
          <h1 className="text-lg font-semibold text-gray-800">Atharva D</h1>
        </div>

        <div className="flex items-center gap-4">
          {/* Notification Bell */}
          <button className="relative p-2 rounded-full hover:bg-gray-100">
            {/* Red Dot Ping */}
            <span className="absolute top-1 right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>

            <Bell className="w-6 h-6 text-gray-600" />
          </button>

          {/* Avatar */}
          <button className="relative p-2 rounded-full hover:bg-gray-100">
            <div className="w-10 h-10 rounded-full bg-violet-200 flex items-center justify-center text-lg">
              <span role="img" aria-label="avatar">
                🧑‍💼
              </span>
            </div>
          </button>
        </div>
      </div>

      {/* Breadcrumb */}
      <p className="mb-4 text-x text-gray-400 ">
        Dashboard &gt;{" "}
        <span className="font-bold text-xl  text-gray-800">Summary</span>
      </p>

      {/* Tabs + Filter */}
      <div className="flex flex-wrap items-center justify-between w-[78vw] gap-4 mb-8 ">
        <div className="flex gap-6">
          {["performance", "safe", "eco"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`text-sm font-semibold capitalize pb-2 transition-colors duration-200 ${
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
        
        <div>
          <select
            value={selectedDays}
            onChange={(e) => setSelectedDays(Number(e.target.value))}
            className="border border-green-600 text-green-600 bg-white  py-1.5 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value={7}>Last 7 Days</option>
            <option value={14}>Last 14 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={60}>Last 60 Days</option>
          </select>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 mb-8 w-[78vw]">
        {getCurrentTabData().map((stat) => (
          <div
            key={stat.metric}
            className="bg-white mb-4  rounded-xl shadow-sm px-6 py-5 hover:shadow-md transition-shadow"
          >
            <p className="text-sm text-gray-400">{stat.metric}</p>
            <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
          </div>
        ))}
      </div>

      

      {/* Chart + Tables Section */}
      <div className="space-y-8 w-[80vw]">
        <div className=" ">
          <BarChartGraph selectedDays={selectedDays} />
        </div>

        <div className=" w-[80vw] ">
          <Dashboard selectedDays={selectedDays} />
          Accurate Group
        </div>

        <div className=" p-">
          <TopDriversTable top10Aggresive={top10Aggresive} />
        </div>

        <div className=" p-">
          <TopDriversTable top10Aggresive={top10Safe} />
        </div>
      </div>
    </div>
  );
};

export default Summary;
