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

import React from "react";
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

  const metrics = [
    {
      title: "Safety Score",
      value: "79.81",
      unit: "",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Trust Level",
      value: "100",
      unit: "",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Trips",
      value: "19",
      unit: "",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Mileage",
      value: "1",
      unit: "",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Time Drive",
      value: "7.36",
      unit: "hr",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Average Speed",
      value: "12.78",
      unit: "mh",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Max Speed",
      value: "66.74",
      unit: "mh",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Phone Usage",
      value: "0.00",
      unit: "%",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Speeding",
      value: "0.74",
      unit: "%",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Phone Usage Speed",
      value: "0.37",
      unit: "%",
      subtitle: "Last Month",
      change: "+12%",
    },
    {
      title: "Unique Tags Count",
      value: "1",
      unit: "",
      subtitle: "Last Month",
      change: "+12%",
    },
  ];

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
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  const radarData = {
  labels: ["Speed", "Braking", "Turning", "Acceleration", "Fuel", "Safety"],
  datasets: [
    {
      label: "Driver A",
      data: [65, 59, 90, 81, 56, 55],
      backgroundColor: "rgba(75,192,192,0.2)",
      borderColor: "rgba(75,192,192,1)",
      borderWidth: 2,
    },
  
  ],
};

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
      <div className="flex justify-between items-center mb-6">
        <p className="md:w-[204px] md:h-[30px] font-medium text-gray-400 mb-[23px]">
          Dashboard &gt;{" "}
          <span className="font-bold text-xl text-gray-800">Safety</span>
        </p>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
            Export as PDF
          </button>
          <select className="px-3 py-2 border rounded-md">
            <option>Last Year</option>
            <option>Last Month</option>
            <option>Last Week</option>
          </select>
        </div>
      </div>

      {/* Metrics */}
      <div
        className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3  
        xl:grid-cols-4 2xl:grid-cols-6 gap-8 mb-8"
      >
        {metrics.map((m, idx) => (
          <div
            key={idx}
            className="flex flex-col justify-between bg-white
                      rounded-xl shadow-sm hover:shadow-md transition-shadow
                      p-4 md:p-8 gap-4
                      2xl:max-w-[209px] 2xl:max-h-[192px]"
          >
            {/* Title */}
            <p className="text-sm font-medium text-gray-400">{m.title}</p>

            {/* Value */}
            <h2 className="text-4xl font-bold text-gray-800">
              {m.value}
              {m.unit}
            </h2>

            {/* Subtext + Change */}
            <div className="flex items-center justify-between text-sm">
              <p className="text-gray-800">{m.subtitle}</p>
              {m.change && (
                <span
                  className={`text-xs px-2 py-1 rounded-xl ${
                    m.change.startsWith("-")
                      ? "text-red-500"
                      : "font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl"
                  }`}
                >
                  {m.change}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Safety Parameters */}

      <div className="flex justify-between items-center mb-1">
        <h2 className="font-medium">Safety Parameters</h2>
      </div>

      <div className="bg-white pt-4 rounded-lg p-4">
        <div>
          <span className=" gap-8  m-6">
            {/* Safety Parametrs:  */}
            <select className="px-4 py-2 border rounded-md text-sm ">
              <option>Safety Score</option>
              <option>Acceleration</option>
              <option>Phone usage</option>
            </select>{" "}
          </span>
        </div>
       <div
       className=" pt-4"> <Line data={data} options={options} height={100} /></div>
      </div>

      <div className="flex flex-wrap gap-10 2xl:max-w-[1830px] mb-8  mt-7 ">
        {/* Chart 1 */}
        <div className="flex-1 min-w-[300px] h-[400px] pt-2 bg-white pb-10 pl-8 rounded-lg">
          <span className="block mb-2 font-medium">Mileage Daily (mi)</span>
          <Line
            data={data1}
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

        {/* Chart 2 */}
        {/* <div className="flex-1 min-w-[300px] h-[400px] bg-white  pb-10 pl-8 rounded-lg">
          <span className="block mb-2 font-medium pt-2">Driving Time Daily (mi)</span>
          <Line
            data={data1}
            options={{
              ...options1,
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        </div> */}
      </div>

    </div>
  );
};

export default Dashboard;
