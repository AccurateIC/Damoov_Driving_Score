// // import { useEffect, useState } from "react";
// // import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// // const Safety = () => {
// //   const [metrics, setMetrics] = useState(null);

// //   useEffect(() => {
// //     fetch("http://127.0.0.1:5000/safety_dashboard_summary?filter=last_1_month")
// //       .then((res) => res.json())
// //       .then((data) => setMetrics(data))
// //       .catch((err) => console.error("Error fetching metrics:", err));
// //   }, []);

// //   const chartData = [
// //     { month: "Jan", value: 10 },
// //     { month: "Feb", value: 30 },
// //     { month: "Mar", value: 50 },
// //     { month: "Apr", value: 75 },
// //     { month: "May", value: 40 },
// //     { month: "Jun", value: 50 },
// //     { month: "Jul", value: 45 },
// //     { month: "Aug", value: 60 },
// //     { month: "Sep", value: 95 },
// //     { month: "Oct", value: 70 },
// //     { month: "Nov", value: 40 },
// //     { month: "Dec", value: 55 },
// //   ];

// //   if (!metrics) return <p className="p-6">Loading...</p>;

// //   const metricsList = [
// //     { title: "Safety Score", value: metrics.safety_score.toFixed(2), unit: "" },
// //     { title: "Trips", value: metrics.trips, unit: "" },
// //     { title: "Driver Trips", value: metrics.driver_trips, unit: "" },
// //     { title: "Mileage", value: metrics.mileage_km.toFixed(2), unit: " km" },
// //     { title: "Time Driven", value: (metrics.time_driven_minutes / 60).toFixed(2), unit: " hr" },
// //     { title: "Average Speed", value: metrics.average_speed_kmh.toFixed(2), unit: " km/h" },
// //     { title: "Max Speed", value: metrics.max_speed_kmh.toFixed(2), unit: " km/h" },
// //     { title: "Phone Usage", value: metrics.phone_usage_percentage.toFixed(2), unit: "%" },
// //     { title: "Speeding", value: metrics.speeding_percentage.toFixed(2), unit: "%" },
// //     { title: "Phone Usage Speeding", value: metrics.phone_usage_speeding_percentage.toFixed(2), unit: "%" },
// //     { title: "Unique Tags Count", value: metrics.unique_tags_count, unit: "" },
// //   ];

// //   return (
// //     <div className="p-6 bg-gray-50 min-h-screen">
// //       {/* Header */}
// //       <div className="flex justify-between items-center mb-6">
// //         <h1 className="text-lg font-semibold">
// //           Dashboard: <span className="font-bold">Safety</span>
// //         </h1>
// //         <div className="flex gap-2">
// //           <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">Export as PDF</button>
// //           <select className="px-3 py-2 border rounded-md">
// //             <option>Last Month</option>
// //             <option>Last Year</option>
// //           </select>
// //         </div>
// //       </div>

// //       {/* Metrics Grid */}
// //       <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
// //         {metricsList.map((m, idx) => (
// //           <div key={idx} className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
// //             <h2 className="text-xl font-bold">{m.value}{m.unit}</h2>
// //             <p className="text-gray-500 text-sm">{m.title}</p>
// //             <p className="text-xs text-gray-400">Last Month</p>
// //             <span className="text-green-500 text-xs">+12%</span>
// //           </div>
// //         ))}
// //       </div>

// //       {/* Safety Parameters (Chart) */}
// //       <div className="bg-white rounded-xl shadow p-6">
// //         <h2 className="mb-4 font-medium">Safety Parameters</h2>
// //         <ResponsiveContainer width="100%" height={300}>
// //           <LineChart data={chartData}>
// //             <XAxis dataKey="month" />
// //             <YAxis />
// //             <Tooltip />
// //             <Line type="monotone" dataKey="value" stroke="#4f46e5" strokeWidth={2} dot />
// //           </LineChart>
// //         </ResponsiveContainer>
// //       </div>
// //     </div>
// //   );
// // };

// // export default Safety;

// import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// const Dashboard = () => {
//   const data = [
//     { month: "Jan", value: 10 },
//     { month: "Feb", value: 30 },
//     { month: "Mar", value: 50 },
//     { month: "Apr", value: 75 },
//     { month: "May", value: 40 },
//     { month: "Jun", value: 50 },
//     { month: "Jul", value: 45 },
//     { month: "Aug", value: 60 },
//     { month: "Sep", value: 95 },
//     { month: "Oct", value: 70 },
//     { month: "Nov", value: 40 },
//     { month: "Dec", value: 55 },
//   ];

//   const metrics = [
//     { title: "Safety Score", value: "79.81", unit: "", subtitle: "Last Month", change: "+12%" },
//     { title: "Trust Level", value: "100", unit: "", subtitle: "Last Month", change: "+12%" },
//     { title: "Trips", value: "19", unit: "", subtitle: "Last Month", change: "+12%" },
//     { title: "Mileage", value: "1", unit: "", subtitle: "Last Month", change: "+12%" },
//     { title: "Time Drive", value: "7.36", unit: "hr", subtitle: "Last Month", change: "+12%" },
//     { title: "Average Speed", value: "12.78", unit: "mh", subtitle: "Last Month", change: "+12%" },
//     { title: "Max Speed", value: "66.74", unit: "mh", subtitle: "Last Month", change: "+12%" },
//     { title: "Phone Usage", value: "0.00", unit: "%", subtitle: "Last Month", change: "+12%" },
//     { title: "Speeding", value: "0.74", unit: "%", subtitle: "Last Month", change: "+12%" },
//     { title: "Phone Usage Speed", value: "0.37", unit: "%", subtitle: "Last Month", change: "+12%" },
//     { title: "Unique Tags Count", value: "1", unit: "", subtitle: "Last Month", change: "+12%" },
//   ];

//   return (
// //   <div className="px-12 bg-gray-50 min-h-screen">
// //   {/* Header */}
// //   <div className="flex justify-between items-center mb-6">
// //     <p className="md:w-[204px]  md:h-[30px] font-medium text-gray-400 mb-[23px]">
// //             Dashboard &gt;{" "}
// //             <span className="font-bold text-xl  text-gray-800">Safety</span>
// //           </p>
// //     <div className="flex gap-2">
// //       <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
// //         Export as PDF
// //       </button>
// //       <select className="px-3 py-2 border rounded-md">
// //         <option>Last Year</option>
// //         <option>Last Month</option>
// //         <option>Last Week</option>
// //       </select>
// //     </div>
// //   </div>

// //   {/* Metrics */}
// //   <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3
// //   xl:grid-cols-4 2xl:grid-cols-6 gap-8 mb-8">
// //     {metrics.map((m, idx) => (
// //       <div
// //         key={idx}
// //         className="flex flex-col justify-between bg-amber-400
// //                    rounded-xl shadow-sm hover:shadow-md transition-shadow
// //                    p-4 md:p-8    gap-4 p-8
// //                    2xl:max-w-[209px] 2xl:max-h-[192px]"
// //       >
// //         {/* Title */}
// //         <p className="text-sm font-medium text-gray-400">{m.title}</p>

// //         {/* Value */}
// //         <h2 className="text-4xl font-bold text-gray-800">
// //           {m.value}
// //           {m.unit}
// //         </h2>

// //         {/* Subtext + Change */}
// //         <div className="flex items-center justify-between text-sm">
// //           <p className="text-gray-800">{m.subtitle}</p>
// //           {m.change && (
// //             <span
// //               className={`text-xs px-2 py-1 rounded-xl ${
// //                 m.change.startsWith("-")
// //                   ? " text-red-500"
// //                   : "font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl"
// //               }`}
// //             >
// //               {m.change}
// //             </span>
// //           )}
// //         </div>
// //       </div>
// //     ))}
// //   </div>

// //   {/* Safety Parameters */}
// //   <div className="bg-white rounded-xl shadow p-6 2xl:min-h-[582px] mb-4">
// //     <h2 className="mb-4 font-medium">Safety Parameters</h2>
// //     <ResponsiveContainer width="100%" height={500}>
// //       <LineChart data={data}>
// //         <XAxis dataKey="month" />
// //         <YAxis />
// //         <Tooltip />
// //         <Line
// //           type="monotone"
// //           dataKey="value"
// //           stroke="#4f46e5"
// //           strokeWidth={2}
// //           dot
// //         />
// //       </LineChart>
// //     </ResponsiveContainer>
// //   </div>
// // </div>
// <div className="px-12

//   bg-amber-300 min-h-screen">
//   {/* Header */}
//   <div className="flex justify-between items-center mb-6 bg-amber-600">
//     <p className="md:w-[204px] md:h-[30px] font-medium text-gray-400 mb-[23px]">
//       Dashboard &gt;{" "}
//       <span className="font-bold text-xl text-gray-800">Safety</span>
//     </p>
//     <div className="flex gap-2">
//       <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
//         Export as PDF
//       </button>
//       <select className="px-3 py-2 border rounded-md">
//         <option>Last Year</option>
//         <option>Last Month</option>
//         <option>Last Week</option>
//       </select>
//     </div>
//   </div>

//   {/* Metrics */}
//   <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3  bg-amber-600
//   xl:grid-cols-4 2xl:grid-cols-6 gap-8 mb-8">
//     {metrics.map((m, idx) => (
//       <div
//         key={idx}
//         className="flex flex-col justify-between bg-white
//                    rounded-xl shadow-sm hover:shadow-md transition-shadow
//                    p-4 md:p-8 gap-4
//                    2xl:max-w-[209px] 2xl:max-h-[192px]"
//       >
//         {/* Title */}
//         <p className="text-sm font-medium text-gray-400">{m.title}</p>

//         {/* Value */}
//         <h2 className="text-4xl font-bold text-gray-800">
//           {m.value}
//           {m.unit}
//         </h2>

//         {/* Subtext + Change */}
//         <div className="flex items-center justify-between text-sm">
//           <p className="text-gray-800">{m.subtitle}</p>
//           {m.change && (
//             <span
//               className={`text-xs px-2 py-1 rounded-xl ${
//                 m.change.startsWith("-")
//                   ? "text-red-500"
//                   : "font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl"
//               }`}
//             >
//               {m.change}
//             </span>
//           )}
//         </div>
//       </div>
//     ))}
//   </div>

//   {/* Safety Parameters */}
//   <div className=" rounded-xl shadow p-6 2xl:min-h-[582px] mb-4 bg-amber-600">
//     {/* Title + Dropdown */}
//     <div className="flex justify-between items-center mb-4">
//       <h2 className="font-medium">Safety Parameters</h2>
//       <select className="px-3 py-2 border rounded-md text-sm">
//         <option>Last Year</option>
//         <option>Last Month</option>
//         <option>Last Week</option>
//       </select>
//     </div>

//     {/* Chart */}
//     <ResponsiveContainer width="100%" height={500}>
//       <LineChart data={data}>
//         <XAxis dataKey="month" />
//         <YAxis />
//         <Tooltip />
//         <Line
//           type="monotone"
//           dataKey="value"
//           stroke="#4f46e5"
//           strokeWidth={2}
//           dot
//         />
//       </LineChart>
//     </ResponsiveContainer>
//   </div>

//   <div className=" bg-amber-700 ">
//  <div className=" rounded-xl shadow p-6 2xl:min-h-[582px] mb-4 bg-amber-600">
//     {/* Title + Dropdown */}
//     <div className="flex justify-between items-center mb-4">
//       <h2 className="font-medium">Safety Parameters</h2>
//       <select className="px-3 py-2 border rounded-md text-sm">
//         <option>Last Year</option>
//         <option>Last Month</option>
//         <option>Last Week</option>
//       </select>
//     </div>

//     {/* Chart */}
//     <ResponsiveContainer width="100%" height={500}>
//       <LineChart data={data}>
//         <XAxis dataKey="month" />
//         <YAxis />
//         <Tooltip />
//         <Line
//           type="monotone"
//           dataKey="value"
//           stroke="#4f46e5"
//           strokeWidth={2}
//           dot
//         />
//       </LineChart>
//     </ResponsiveContainer>
//   </div>

//   </div>
// </div>

//   );
// };

// export default Dashboard;

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

const baseURL = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:5000";
const Dashboard = () => {
  const data = {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Safety Parameters",
        data: [10, 30, 50, 75, 40, 50, 45, 60, 95, 70, 40, 55],
        borderColor: "#4f46e5",
        backgroundColor: "rgba(79, 70, 229, 0.2)",
        tension: 0.4,
        fill: true,
        pointRadius: 4,
      },
    ],
  };

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

  // const metrics = [
  //   {
  //     title: "Safety Score",
  //     value: "79.81",
  //     unit: "",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Trust Level",
  //     value: "100",
  //     unit: "",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Trips",
  //     value: "19",
  //     unit: "",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Mileage",
  //     value: "1",
  //     unit: "",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Time Drive",
  //     value: "7.36",
  //     unit: "hr",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Average Speed",
  //     value: "12.78",
  //     unit: "mh",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Max Speed",
  //     value: "66.74",
  //     unit: "mh",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Phone Usage",
  //     value: "0.00",
  //     unit: "%",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Speeding",
  //     value: "0.74",
  //     unit: "%",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Phone Usage Speed",
  //     value: "0.37",
  //     unit: "%",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  //   {
  //     title: "Unique Tags Count",
  //     value: "1",
  //     unit: "",
  //     subtitle: "Last Month",
  //     change: "+12%",
  //   },
  // ];
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
  "Acceleration": "acc_score",
  "Phone usage": "phone_score",
  "Deceleration":"dec_score",
  "Cornering": "cor_score",
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
            borderColor: "rgba(75,192,192,1)",
            backgroundColor: "rgba(75,192,192,0.2)",
            tension: 0.4,
            fill: true,
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
              borderColor: "rgba(75,192,192,1)",
              backgroundColor: "rgba(75,192,192,0.2)",
              tension: 0.4,
              fill: true,
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



  const data1 = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sept"],
    datasets: [
      {
        label: "Sales",
        data: [10, 20, 15, 30, 25, 40, 15, 90, 40],
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(75,192,192,0.2)",
        tension: 0.4, // smooth curve
        fill: true,
      },
    ],
  };

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


  const radarData = {
  labels: ["Speed", "Braking", "Turning", "Acceleration", "Fuel", "Safety"],
  datasets: [
    {
      label: "Driving Trips Params",
      data: [65, 59, 90, 81, 56, 55],
      backgroundColor: "rgba(75,192,192,0.2)",
      borderColor: "rgba(75,192,192,1)",
      borderWidth: 2,
    },
  ],
}



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
    <div className="px-12  min-h-screen">
      {/* Header */}
      <div className="flex  justify-between items-center mb-6">
        <p className="md:w-[204px] md:h-[30px] font-medium text-gray-400 mb-[23px]">
          Dashboard &gt;{" "}
          <span className="font-bold text-xl text-gray-800">Safety</span>
        </p>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
            Export as PDF
          </button>
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

    
       <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3  
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
            <h2 className="text-4xl font-bold text-gray-800">
              {m.value}
            </h2>
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
        className="px-4 py-2 border rounded-md text-sm"
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

  <div className="pt-4">
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
          <span className="block mb-2 font-medium">Driving Time Daily (mi)</span>
          <Line
            data={data1}
            options={{
              ...options1,
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        </div>
      </div>

      <div className="flex flex-wrap  2xl:max-w-[1830px] mb-8 gap-10 mt-7 ">
        {/* Chart 1 */}
      <div className="flex-1 max-w-[735px] h-[400px] pt-2 bg-white pb-10 pl-8 rounded-lg">
  <span className="block mb-2 font-medium">Driving Trips Daily</span>
  <Radar data={radarData} options={radarOptions} />
</div>

     
      </div>

    </div>
  );
};

export default Dashboard;




// // DashboardWithTimeFilter.jsx
// import React, { useState, useMemo } from "react";
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend,
//   RadialLinearScale,
//   Filler,
// } from "chart.js";
// import { Line, Radar } from "react-chartjs-2";

// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   RadialLinearScale,
//   Title,
//   Tooltip,
//   Legend,
//   Filler
// );

// const DashboardWithTimeFilter = () => {
//   // --- UI state ---
//   const [period, setPeriod] = useState("last_month"); // last_week | last_month | last_year
//   const [safetyParam, setSafetyParam] = useState("Safety Score"); // chosen metric for safety chart

//   // --- Dummy data for each period ---
//   const months = [
//     "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
//   ];

//   const periodData = {
//     last_week: {
//       labels: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
//       mileage: [12, 18, 10, 22, 30, 25, 28],
//       drivingTime: [40, 45, 30, 50, 70, 55, 60],
//       safetyParams: {
//         "Safety Score": [72, 74, 76, 75, 78, 80, 82],
//         Acceleration: [55, 60, 58, 62, 67, 71, 68],
//         "Phone usage": [3, 2, 4, 1, 2, 3, 2],
//       },
//       radar: [78, 65, 70, 74, 80, 72],
//     },
//     last_month: {
//       labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
//       mileage: [320, 420, 380, 450],
//       drivingTime: [1200, 1350, 1280, 1400],
//       safetyParams: {
//         "Safety Score": [74, 76, 78, 79],
//         Acceleration: [60, 62, 65, 63],
//         "Phone usage": [2.5, 3.0, 2.2, 2.8],
//       },
//       radar: [80, 70, 68, 76, 82, 75],
//     },
//     last_year: {
//       labels: months,
//       mileage: [900, 1100, 950, 1200, 1300, 1250, 1400, 1500, 1600, 1550, 1450, 1350],
//       drivingTime: [3200, 3600, 3300, 4000, 4200, 4100, 4300, 4500, 4700, 4600, 4400, 4200],
//       safetyParams: {
//         "Safety Score": [70,72,74,75,76,78,79,81,83,82,80,79],
//         Acceleration: [58,60,62,60,61,63,66,68,70,69,67,65],
//         "Phone usage": [4,4.2,4.0,3.8,3.5,3.1,2.9,2.7,2.5,2.6,2.8,3.0],
//       },
//       radar: [82, 75, 72, 78, 85, 80],
//     },
//   };

//   // --- Chart datas built from the active period (useMemo for perf) ---
//   const safetyLineData = useMemo(() => {
//     const pd = periodData[period];
//     return {
//       labels: pd.labels,
//       datasets: [
//         {
//           label: safetyParam,
//           data: pd.safetyParams[safetyParam],
//           borderColor: "#4f46e5",
//           backgroundColor: "rgba(79,70,229,0.15)",
//           tension: 0.35,
//           fill: true,
//           pointRadius: 3,
//           pointHoverRadius: 5,
//         },
//       ],
//     };
//   }, [period, safetyParam]);

//   const mileageData = useMemo(() => {
//     const pd = periodData[period];
//     return {
//       labels: pd.labels,
//       datasets: [
//         {
//           label: "Mileage",
//           data: pd.mileage,
//           borderColor: "#10b981", // green
//           backgroundColor: "rgba(16,185,129,0.12)",
//           tension: 0.3,
//           fill: true,
//           pointRadius: 2,
//         },
//       ],
//     };
//   }, [period]);

//   const drivingTimeData = useMemo(() => {
//     const pd = periodData[period];
//     return {
//       labels: pd.labels,
//       datasets: [
//         {
//           label: "Driving Time",
//           data: pd.drivingTime,
//           borderColor: "#3b82f6", // blue
//           backgroundColor: "rgba(59,130,246,0.12)",
//           tension: 0.3,
//           fill: true,
//           pointRadius: 2,
//         },
//       ],
//     };
//   }, [period]);

//   const radarChartData = useMemo(() => {
//     const pd = periodData[period];
//     return {
//       labels: ["Acceleration","Phone Usage","Speeding","Cornering","Braking","Handling"],
//       datasets: [
//         {
//           label: "Driving Params",
//           data: pd.radar,
//           borderColor: "#6366f1",
//           backgroundColor: "rgba(99,102,241,0.18)",
//           pointBackgroundColor: "#6366f1",
//           borderWidth: 2,
//         },
//       ],
//     };
//   }, [period]);

//   // --- Chart options (responsive, fill parent card height) ---
//   const lineOptions = {
//     responsive: true,
//     maintainAspectRatio: false, // important so chart fills container height
//     plugins: {
//       legend: { display: false },
//       tooltip: { mode: "index", intersect: false },
//     },
//     scales: {
//       x: { grid: { display: false } },
//       y: { beginAtZero: true, grid: { color: "#f3f4f6" } },
//     },
//   };

//   const radarOptions = {
//     responsive: true,
//     maintainAspectRatio: false,
//     scales: {
//       r: {
//         angleLines: { color: "#e5e7eb" },
//         grid: { color: "#e5e7eb" },
//         suggestedMin: 0,
//         suggestedMax: 100,
//       },
//     },
//     plugins: { legend: { display: false } },
//   };

//   // --- Some simple metrics (dummy) ---
//   const metrics = [
//     { title: "Safety Score", value: "79.8", change: "+3%",  subtitle: "Last Month", },
//     { title: "Trust Level", value: "100", change: "—" ,  subtitle: "Last Month",},
//     { title: "Trips", value: "46", change: "+8%",  subtitle: "Last Month", },
//     { title: "Mileage", value: "8.6k km", change: "+5%",  subtitle: "Last Month", },
//     { title: "Time Driven", value: "16.3 hr", change: "+4%",  subtitle: "Last Month", },
//     { title: "Avg Speed", value: "19.5 km/h", change: "—",  subtitle: "Last Month", },
//     {      title: "Max Speed",
//       value: "66.74",
//       unit: "mh",
//       subtitle: "Last Month",
//       change: "+12%",
//     },
//     {
//       title: "Phone Usage",
//       value: "0.00",
//       unit: "%",
//       subtitle: "Last Month",
//       change: "+12%",
//     },
//     {
//       title: "Speeding",
//       value: "0.74",
//       unit: "%",
//       subtitle: "Last Month",
//       change: "+12%",
//     },
//     {
//       title: "Phone Usage Speed",
//       value: "0.37",
//       unit: "%",
//       subtitle: "Last Month",
//       change: "+12%",
//     },
//     {
//       title: "Unique Tags Count",
//       value: "1",
//       unit: "",
//       subtitle: "Last Month",
//       change: "+12%",
//     },
//   ];

//   return (
//     <div className="px-12 min-h-screen">
//       {/* Header + Period selector */}
//       <div className="flex justify-between items-center mb-6">
//         <p className="md:w-[204px] md:h-[30px] font-medium text-gray-600 mb-[4px]">
//           Dashboard &gt;{" "}
//           <span className="font-bold text-xl text-gray-800">Safety</span>
//         </p>

//         <div className="flex items-center gap-3">
//           <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
//             Export as PDF
//           </button>

//           {/* Period dropdown (controls ALL charts) */}
//           <select
//             value={period}
//             onChange={(e) => setPeriod(e.target.value)}
//             className="px-3 py-2 border rounded-md text-sm"
//           >
//             <option value="last_week">Last Week</option>
//             <option value="last_month">Last Month</option>
//             <option value="last_year">Last Year</option>
//           </select>
//         </div>
//       </div>

//       {/* Metrics cards (top) */}
//       {/* <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-6">
//         {metrics.map((m, idx) => (
//           <div
//             key={idx}
//             className="bg-white rounded-xl shadow p-4 flex  items-center"
//           >
//             <div className="text-2xl font-semibold  text-gray-800">{m.value}</div>
//             <div className="text-sm text-gray-500">{m.title}</div>
//                <div className="flex items-center justify-between text-sm">
//                <p className="text-gray-800">{m.subtitle}</p>
//               {m.change && (
//                 <span
//                   className={`text-xs px-2 py-1 rounded-xl ${
//                     m.change.startsWith("-")
//                       ? "text-red-500"
//                       : "font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl"
//                   }`}
//                 >
//                   {m.change}
//                 </span>
//               )}
//             </div>
//           </div>
//         ))}
//       </div> */}
//       <div className="grid grid-cols-1 bg- sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-6">
//   {metrics.map((m, idx) => (
//     <div
//       key={idx}
//       className="bg-white rounded-xl  shadow p-4 flex flex-col items-center justify-between"
//     >
//       {/* Title */}
//       <p className="text-sm text-gray-500 mb-1">{m.title}</p>

//       {/* Value */}
//       <h3 className="text-2xl font-bold text-gray-900">{m.value} {m.unit}</h3>

//       {/* Subtitle + Change */}
//       <div className="flex items-center gap-4 mt-3">
//         <p className="text-xs text-gray-500">{m.subtitle}</p>
//         {m.change && (
//           <span
//             className={`text-xs font-medium px-2 py-0.5 rounded-lg ${
//               m.change.startsWith("-")
//                 ? "text-red-600 bg-red-50 border border-red-200"
//                 : "text-green-600 bg-green-50 border border-green-200"
//             }`}
//           >
//             {m.change}
//           </span>
//         )}
//       </div>
//     </div>
//   ))}
// </div>


//       {/* Safety Parameters card */}
//       <div className="bg-white rounded-xl shadow p-4 mb-6">
//         <div className="flex gap-4 items-center mb-4">
//           <h2 className="font-medium">Safety Parameters</h2>

//           {/* This select chooses which safety metric to plot in the safety line */}
//           <select
//             value={safetyParam}
//             onChange={(e) => setSafetyParam(e.target.value)}
//             className="px-3 py-2 border rounded-md text-sm"
//           >
//             <option>Safety Score</option>
//             <option>Acceleration</option>
//             <option>Phone usage</option>
//           </select>
//         </div>

//         {/* Safety line chart - fills card height */}
//         <div className="h-[260px] md:h-[320px]">
//           <Line data={safetyLineData} options={lineOptions} />
//         </div>
//       </div>

//       {/* Two side-by-side charts: Mileage & Driving Time */}
//       <div className="flex flex-wrap gap-6 mb-6">
//         <div className="flex-1 min-w-[280px] h-[360px] bg-white p-4 rounded-lg shadow">
//           <div className="mb-2 font-medium">Mileage Daily</div>
//           <div className="h-[300px]">
//             <Line data={mileageData} options={lineOptions} />
//           </div>
//         </div>

//         <div className="flex-1 min-w-[280px] h-[360px] bg-white p-4 rounded-lg shadow">
//           <div className="mb-2 font-medium">Driving Time Daily</div>
//           <div className="h-[300px]">
//             <Line data={drivingTimeData} options={lineOptions} />
//           </div>
//         </div>
//       </div>

//       {/* Radar chart */}
//       <div className="flex flex-wrap gap-6">
//         <div className="flex-1 min-w-[320px] h-[420px] 2xl:max-w-[735px] bg-white p-4 rounded-lg shadow">
//           <div className="mb-2 font-medium">Driving Trips (Radar)</div>
//           <div className="h-[330px]">
//             <Radar data={radarChartData} options={radarOptions} />
//           </div>

//           {/* small labels + scores */}
//           {/* <div className="grid grid-cols-2  gap-2 mt-4 text-sm text-gray-700">
//             {["Acceleration","Phone Usage","Speeding","Cornering","Braking","Handling"].map((lab, i) => (
//               <div key={lab} className="flex items-center justify-between">
//                 <span>{lab}</span>
//                 <span className="font-bold text-indigo-600">{radarChartData.datasets[0].data[i]}</span>
//               </div>
//             ))}
//           </div> */}
//         </div>

//         {/* Placeholder: you can add another chart here if you want */}
//         {/* <div className="flex-1 min-w-[320px] h-[420px] bg-white p-4 rounded-lg shadow">
//           <div className="mb-2 font-medium">Extra Chart</div>
//           <div className="h-[330px]">
           
//             <Line data={mileageData} options={lineOptions} />
//           </div>
//         </div> */}
//       </div>
//     </div>
//   );
// };

// export default DashboardWithTimeFilter;
