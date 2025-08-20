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
    const filterValue = getFilterValue(30);
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
  }, [30]);

  const [safeDrivingData, setSafeDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  useEffect(() => {
    const filterValue = getFilterValue(30);
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
  }, [30]);

  const [ecoDrivingData, setEcoDrivingData] = useState<
    { metric: string; value: string }[]
  >([]);

  useEffect(() => {
    const filterValue = getFilterValue(30);

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
  }, [30]);

  const getCurrentTabData = () => {
    if (activeTab === "safe") return safeDrivingData;
    if (activeTab === "eco") return ecoDrivingData;
    return performanceData;
  };
  return (
    <div className="bg-gray-50 min-h-screen py-8 px-4 md:px-12 font-inter">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div>
          <div className="text-xs text-gray-400 mb-1">Good Morning,</div>
          <div className="text-lg font-semibold text-gray-800">Atharva D</div>
        </div>
        <div className="w-10 h-10 rounded-full bg-violet-200 flex items-center justify-center">
          <span role="img" aria-label="avatar">
            🧑‍💼
          </span>
        </div>
      </div>
      <div className="mb-2 text-xs text-gray-400">
        Dashboard &gt;{" "}
        <span className="font-semibold text-gray-800">Summary</span>
      </div>

      {/* Tabs */}
      <div className="flex gap-8 mb-8 border-b border-gray-200">
       
        {["performance", "safe", "eco"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            className={`text-sm font-semibold capitalize pb-2 ${
              activeTab === tab
                ? "text-blue-600 border-b-4 border-blue-600"
                : "text-gray-500 hover:text-gray-700"
            } transition-colors duration-200`}
          >
            {tab === "performance"
              ? "Performance"
              : tab === "safe"
              ? "Safe Driving"
              : "Eco Driving"}
          </button>
        ))}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 mb-8">
        {getCurrentTabData().map((stat) => (
          <div
            key={stat.metric}
            className="bg-white rounded-xl shadow-sm px-6 py-5"
          >
            <div className="text-sm text-gray-400">{stat.metric}</div>
            <div className="text-2xl font-bold text-gray-800">{stat.value}</div>

            {/* Optional period and trend */}
          </div>
        ))}
      </div>

      {/* Chart Card */}
      
     
        <div>
       <BarChartGraph />
        {/* <OverviewChart  /> */}
        
      </div>
    </div>
  );
};

export default Summary;
