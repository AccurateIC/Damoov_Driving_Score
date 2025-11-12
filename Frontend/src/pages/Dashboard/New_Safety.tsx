

import React, { useEffect, useState } from "react";
import axios from "axios";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { Radar } from "react-chartjs-2";
import { Filter } from "lucide-react";
import Breadcrumbs from "./Breadcrumbs";


// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const baseURL = import.meta.env.VITE_BASE_URL;
const Dashboard = () => {
  // const data = {
  //   labels: [
  //     "Jan",
  //     "Feb",
  //     "Mar",
  //     "Apr",
  //     "May",
  //     "Jun",
  //     "Jul",
  //     "Aug",
  //     "Sep",
  //     "Oct",
  //     "Nov",
  //     "Dec",
  //   ],
  //   datasets: [
  //     {
  //       label: "Safety Parameters",
  //       data: [10, 30, 50, 75, 40, 50, 45, 60, 95, 70, 40, 55],
  //       borderColor: "##6976EB",
  //       backgroundColor: "rgba(79, 70, 229, 0.2)",
  //       tension: 0.4,
  //       fill: true,
  //       pointRadius: 4,
  //     },
  //   ],
  // };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const mapApiResponseToMetrics = (data) => [
    {
      title: "Safety Score",
      value: data.safety_score?.toFixed(2),
      unit: "",
      subtitle: "Selected Period",
    },
    {
      title: "Trust Level",
      value: "100", // not in API response → maybe fixed or calculate separately
      unit: "",
      subtitle: "Selected Period",
    },
    {
      title: "Trips",
      value: data.trips,
      unit: "",
      subtitle: "Selected Period",
    },
    {
      title: "Mileage",
      value: data.mileage_km?.toFixed(2),
      unit: "km",
      subtitle: "Selected Period",
    },
    {
      title: "Time Drive",
      value: (data.time_driven_minutes / 60).toFixed(2),
      unit: "hr",
      subtitle: "Selected Period",
    },
    {
      title: "Average Speed",
      value: data.average_speed_kmh?.toFixed(2),
      unit: "km/h",
      subtitle: "Selected Period",
    },
    {
      title: "Max Speed",
      value: data.max_speed_kmh?.toFixed(2),
      unit: "km/h",
      subtitle: "Selected Period",
    },
    {
      title: "Phone Usage",
      value: data.phone_usage_percentage?.toFixed(2),
      unit: "%",
      subtitle: "Selected Period",
    },
    {
      title: "Speeding",
      value: data.speeding_percentage?.toFixed(2),
      unit: "%",
      subtitle: "Selected Period",
    },
    {
      title: "Phone Usage Speed",
      value: data.phone_usage_speeding_percentage?.toFixed(2),
      unit: "%",
      subtitle: "Selected Period",
    },
    {
      title: "Unique Tags Count",
      value: data.unique_tags_count,
      unit: "",
      subtitle: "Selected Period",
    },
  ];

  const [metrics, setMetrics] = useState([]);
  const [filter, setFilter] = useState("last_1_month"); // default

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await axios.get(
          `${baseURL}/safety_dashboard_summary?filter=${filter}`
        );
        console.log(res.data);
        setMetrics(mapApiResponseToMetrics(res.data));
        console.log("metrics", metrics);
      } catch (err) {
        console.error("Error fetching metrics:", err);
      }
    };

    fetchMetrics();
  }, [filter]);

  const [metric, setMetric] = useState("safe_score");
  const [chartData, setChartData] = useState(null);

  // dropdown options → API metric keys
  const metricMap = {
    "Safety Score": "safe_score",
    Acceleration: "acc_score",
    "Phone usage": "phone_score",
    Deceleration: "dec_score",
    Cornering: "cor_score",
  };

  useEffect(() => {
    const fetchSafetyParams = async () => {
      try {
        const res = await axios.post(`${baseURL}/safety_graph_trend`, {
          filter_val: filter, // comes from your main filter state
          metric: metric,
        });

        const { data, labels } = res.data;

        setChartData({
          labels,
          datasets: [
            {
              label: metric.replace("_", " ").toUpperCase(),
              data,
              borderColor: "#6976EB",
              // backgroundColor: "#6976EB",
              tension: 0.4,
              // fill: true,
              pointRadius: 4,
            },
          ],
        });
      } catch (err) {
        console.error("Error fetching safety graph:", err);
      }
    };

    fetchSafetyParams();
  }, [filter, metric]);

  const [chartData1, setChartData1] = useState<any>({
    labels: [],
    datasets: [],
  });

  useEffect(() => {
    const fetchMileageDailyParams = async () => {
      try {
        const res = await axios.post(`${baseURL}/mileage_daily`, {
          filter_val: filter,
        });

        console.log("API Response:", res.data);

        const { data, labels } = res.data;

        // Build chart data
        setChartData1({
          labels: labels, // x-axis
          datasets: [
            {
              label: metric.replace("_", " ").toUpperCase(),
              data: data, // y-axis
              borderColor: "#6976EB",
              tension: 0.4,
              // fill: true,
              pointRadius: 4,
            },
          ],
        });
      } catch (err) {
        console.error("Error fetching mileage daily params:", err);
      }
    };

    fetchMileageDailyParams();
  }, [filter, metric]);

  const [dailyTrips, setDailyTrips] = useState<any>({
    labels: [],
    datasets: [],
  });

  useEffect(() => {
    const fetchDrivingTripsDaily = async () => {
      try {
        const res = await axios.post(`${baseURL}/driving_trips_daily`, {
          filter_val: filter,
        });

        console.log("API Response for Daliy  trips :", res.data);

        const { data, labels } = res.data;

        // Build chart data
        setDailyTrips({
          labels: labels, // x-axis
          datasets: [
            {
              label: metric.replace("_", " ").toUpperCase(),
              data: data, // y-axis
              borderColor: "#6976EB",
              tension: 0.4,
              // fill: true,
              pointRadius: 4,
            },
          ],
        });
        console.log("object dailyTrips", dailyTrips);
      } catch (err) {
        console.error("Error fetching mileage daily params:", err);
      }
    };

    fetchDrivingTripsDaily();
  }, [filter]);

  const options1 = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
    },
    scales: {
      x: {
        title: { display: true, text: "Date" },
      },
      y: {
        title: { display: true, text: metric },
      },
    },
  };

  useEffect(() => {
    const fetchDrivingTripsDaily = async () => {
      try {
        const res = await axios.post(`${baseURL}/driving_trips_daily`, {
          filter_val: filter,
        });
        console.log("API Response for Driving Trips Daily:", res.data);
      } catch (err) {
        console.error("Error fetching driving trips daily:", err);
      }
    };
    console.log("Driving Trips Daily Chart Data:");
    fetchDrivingTripsDaily();
  }, [filter]);

  const filterMap: Record<number, string> = {
    7: "last_1_week",
    14: "last_2_weeks",
    30: "last_1_month",
    60: "last_2_months",
  };

  // const [safetyData, setSafetyData] = useState<any[]>([]);
  const [safetyData, setSafetyData] = useState({
    labels: [],
    datasets: [
      {
        label: "Safety Parameters",
        data: [],
        backgroundColor: "#B5B6D5",
        borderColor: "#6976EB",
        tension: 0.4,
        fill: true,
      },
    ],
  });

  useEffect(() => {
    fetch(`${baseURL}/safety_params`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filter_val: filter }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Safety Parma", data);

        const labelsArray = data.labels;
        const dataArray = data.data.map((num: number) =>
          Number(num.toFixed(2))
        );

        const safetyChartData = {
          labels: labelsArray,
          datasets: [
            {
              label: "Safety Parameters",
              data: dataArray,
              backgroundColor: "#B5B6D5",
              borderColor: "#6976EB",
              tension: 0.4,
              fill: true,
            },
          ],
        };

        setSafetyData(safetyChartData);
        console.log("Formatted Safety Data", safetyChartData);
      })
      .catch((err) => {
        console.error("Error fetching safety params:", err);
      });
  }, [filter]);

  const [radarData, setRadarData] = useState({
    labels: [],
    datasets: [
      {
        label: "Safety Parameters",
        data: [],
        backgroundColor: "#B5B6D5",
        borderColor: "#6976EB",
        tension: 0.4,
        fill: true,
      },
    ],
  });

  // const radarData = {
  //   labels: ["Speed", "Braking", "Turning", "Acceleration", "Fuel", "Safety"],
  //   datasets: [
  //     {
  //       label: "Driving Trips Params",
  //       data: [65, 59, 90, 81, 56, 55],
  //       backgroundColor: "#B5B6D5",
  //       borderColor: "#6976EB",
  //       borderWidth: 2,
  //     },
  //   ],
  // };
  const [drivingTimeData, setDrivingTimeData] = useState<any>({
    labels: [],
    datasets: [],
  });
  // useEffect(() => {
  //   fetch(`${baseURL}/driving_time_daily`, {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ filter_val: filter }),
  //   })
  //     })

  useEffect(() => {
    const fetchDrivingTimesDaily = async () => {
      try {
        const res = await axios.post(`${baseURL}/driving_time_daily`, {
          filter_val: filter,
        });

        console.log("API Response for Daliy  trips :", res.data);

        const { data, labels } = res.data;

        // Build chart data
        setDrivingTimeData({
          labels: labels, // x-axis
          datasets: [
            {
              label: metric.replace("_", " ").toUpperCase(),
              data: data, // y-axis
              borderColor: "#6976EB",
              tension: 0.4,
              // fill: true,
              pointRadius: 4,
            },
          ],
        });
        console.log("object dailyTrips", drivingTimeData);
      } catch (err) {
        console.error("Error fetching mileage daily params:", err);
      }
    };
    fetchDrivingTimesDaily();
  }, [filter]);

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: { display: true },
        suggestedMin: 0,
        suggestedMax: 100,
      },
    },
  };

  return (
    <div className="px-12  min-h-screen  bg-gray-200">
      {/* Header */}
      <div className="flex  justify-between items-center mb-6">
        <p className="md:w-[204px] md:h-[30px] font-medium text-gray-400 mb-[23px] ">
          Dashboard &gt;{" "}
          <span className="font-bold text-xl text-gray-800">Safety</span>
        </p>
        <div className="flex gap-2">
          {/* <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
            Export as PDF
          </button> */}
          {/* <select className="px-3 py-2 border rounded-md bg-amber-500">
            <option>Last Year</option>
            <option>Last Month</option>
            <option>Last Week</option>
          </select> */}
          <select
            className="px-3 py-2 border rounded-md "
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="last_1_week">Last Week</option>
            <option value="last_2_weeks">Last 2 Weeks</option>
            <option value="last_1_month">Last Month</option>
            <option value="last_2_months">Last 2 Months</option>
          </select>
        </div>
      </div>

      <div
        className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3  
        xl:grid-cols-4 2xl:grid-cols-6 gap-8 mb-8"
      >
        {metrics.map((m, idx) => (
          <div
            key={idx}
            className="flex flex-col justify-between 
              bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow
              p-4 md:p-8 gap-4 2xl:max-w-[209px] 2xl:max-h-[192px]"
          >
            <p className="text-sm font-medium text-gray-400">{m.title}</p>
            <h2 className="text-4xl font-bold text-gray-800">{m.value}</h2>
            <p className="text-sm text-gray-800">{m.subtitle}</p>
          </div>
        ))}
      </div>

      {/* Safety Parameters */}

      {/* Safety Parameters */}
      <div className="flex justify-between items-center mb-1">
        <h2 className="font-medium">Safety Parameters</h2>
      </div>

      <div className="bg-white  pt-4 rounded-lg p-4">
        <div>
          <span className="gap-8 m-6">
            <select
              className="px-4 py-2 border  rounded-md text-sm"
              value={metric}
              onChange={(e) => setMetric(e.target.value)}
            >
              {Object.entries(metricMap).map(([label, value]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </span>
        </div>

        <div className="pt-4 ">
          {chartData ? (
            <Line data={chartData} options={options} height={100} />
          ) : (
            <p className="text-gray-500 text-sm">Loading chart...</p>
          )}
        </div>
      </div>

      <div className="flex flex-wrap gap-10 2xl:max-w-[1830px] mb-8  mt-7 ">
        {/* Chart 1 */}
        <div className="flex-1 min-w-[300px] h-[400px] pt-2 bg-white pb-10 pl-8 rounded-lg">
          <span className="block mb-2 font-medium">Mileage Daily (mi)</span>
          <Line
            data={chartData1}
            options={{
              ...options1,
              responsive: true,
              maintainAspectRatio: false, // makes it fill container height
            }}
          />
        </div>
        {/* Chart 2 */}
        <div className="flex-1 min-w-[300px] h-[400px] pt-2 bg-white pb-10 pl-8 rounded-lg">
          <span className="block mb-2 font-medium">Driving Trips Daily</span>
          <Line
            data={dailyTrips}
            options={{
              ...options1,
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        </div>
      </div>

      <div className="flex flex-wrap gap-10 2xl:max-w-[1830px] mb-8  mt-7 ">
        {/* Chart 1 */}
        <div className="flex-1 min-w-[300px] h-[400px] pt-2 bg-white pb-10 pl-8 rounded-lg">
          <span className="block mb-2 font-medium">Driving Time Daily</span>
          <Line
            data={drivingTimeData}
            options={{
              ...options1,
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        </div>
        <div className=" flex-1 min-w-[735px] h-[400px] pt-2 bg-white rounded-lg">
          <span className="font-medium p-2"> Safety Parameters</span>
          <Radar data={safetyData} options={radarOptions} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

