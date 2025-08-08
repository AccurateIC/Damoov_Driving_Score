import React, { useEffect, useState, useRef } from "react";
import { Radar, Line } from "react-chartjs-2";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import {
  Chart as ChartJS,
  RadialLinearScale,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  RadialLinearScale,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const Safety = () => {
  const dashboardRef = useRef<HTMLDivElement>(null);

  const [selectedTab, setSelectedTab] = useState("Safety Score");
  // const [selectedDays, setSelectedDays] = useState(14);

  // const metricsTop = [
  //   { label: "Safety Score", value: 65, color: "text-orange-500" },
  //   { label: "Trust Level", value: 100, color: "text-green-500" },
  //   { label: "Trips", value: 6 },
  //   { label: "Driver Trips", value: 6 },
  //   { label: "Mileage mi", value: 46 },
  //   { label: "Time Driven h", value: 5 },
  // ];

// const [metricsTop, setMetricsTop] = useState<
//   { label: string; value: number; color?: string }[]
// >([]);

const [selectedDays, setSelectedDays] = useState(14); // default 14 days
const [metricsTop, setMetricsTop] = useState<
  { label: string; value: number | string; color?: string }[]
>([]);

// Map the select values to your API filter strings
const filterMap: Record<number, string> = {
  7: "last_1_week",
  14: "last_2_weeks",
  30: "last_1_month",
  60: "last_2_months",
};

useEffect(() => {
  const filterValue = filterMap[selectedDays] || "last_2_weeks";

  fetch(`http://127.0.0.1:5000/safety_dashboard_summary?filter=${filterValue}`)
    .then((res) => res.json())
    .then((data) => {
      setMetricsTop([
        { label: "Safety Score", value: data.safety_score, color: "text-orange-500" },
        { label: "Trust Level", value: 100, color: "text-green-500" }, // static
        { label: "Trips", value: data.trips },
        { label: "Driver Trips", value: data.driver_trips },
        { label: "Mileage mi", value: (data.mileage_km * 0.621371).toFixed(2) },
        { label: "Time Driven h", value: (data.time_driven_minutes / 60).toFixed(2) },
      ]);
    })
    .catch((err) => console.error("Error fetching metrics top data:", err));
}, [selectedDays]);



  // const metricsBottom = [
  //   { label: "Average Speed mi/h", value: 34 },
  //   { label: "Max Speed mi/h", value: 62 },
  //   { label: "Phone Usage %", value: 1 },
  //   { label: "Speeding %", value: 8 },
  //   { label: "Phone Usage Speeding %", value: 1 },
  //   { label: "Unique Tags Count", value: "—" },
  // ];

const [metricsBottom, setMetricsBottom] = useState<
  { label: string; value: number | string }[]
>([]);
// const [selectedDays, setSelectedDays] = useState(14); // default filter

// map selectedDays → API filter string
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

  fetch(`http://127.0.0.1:5000/safety_dashboard_summary?filter=${filterValue}`)
    .then((res) => res.json())
    .then((data) => {
      setMetricsBottom([
        {
          label: "Average Speed mi/h",
          value: (data.average_speed_kmh * 0.621371).toFixed(2),
        },
        {
          label: "Max Speed mi/h",
          value: (data.max_speed_kmh * 0.621371).toFixed(2),
        },
        {
          label: "Phone Usage %",
          value: data.phone_usage_percentage.toFixed(2),
        },
        {
          label: "Speeding %",
          value: data.speeding_percentage.toFixed(2),
        },
        {
          label: "Phone Usage Speeding %",
          value: data.phone_usage_speeding_percentage.toFixed(2),
        },
        {
          label: "Unique Tags Count",
          value: data.unique_tags_count ?? "—",
        },
      ]);
    })
    .catch((err) => console.error("Error fetching metrics bottom:", err));
}, [selectedDays]); // runs again when dropdown changes

// Filter dropdown
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



  const tabs = [
    "Safety Score",
    "Acceleration",
    "Braking",
    "Cornering",
    "Speeding",
    "Phone Usage",
  ];

  const radarData = {
    labels: ["Phone usage", "Acceleration", "Brakes", "Cornering", "Speeding"],
    datasets: [
      {
        label: "Safety Metrics",
        data: [100, 100, 100, 100, 100],
        backgroundColor: "rgba(34,197,94,0.3)",
        borderColor: "#22c55e",
        pointBackgroundColor: "#22c55e",
      },
    ],
  };

  const generateLabels = (days: number) => {
    const today = new Date();
    return Array.from({ length: days }, (_, i) => {
      const date = new Date(today);
      date.setDate(today.getDate() - (days - 1 - i));
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
      });
    });
  };

  const generateRandomData = (days: number, min = 10, max = 80) => {
    return Array.from({ length: days }, () =>
      Math.floor(Math.random() * (max - min + 1) + min)
    );
  };

  const commonLabels = generateLabels(selectedDays);
  const lineData = {
    labels: commonLabels,
    datasets: [
      {
        label: `${selectedTab} Daily`,
        data: generateRandomData(selectedDays, 50, 75),
        borderColor: "#22c55e",
        backgroundColor: "rgba(34,197,94,0.2)",
        tension: 0.3,
        fill: true,
      },
    ],
  };

  const dailyMileage = {
    labels: commonLabels,
    datasets: [
      {
        label: "Mileage Daily (mi)",
        data: generateRandomData(selectedDays, 3, 12),
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.2)",
        tension: 0,
        fill: true,
      },
    ],
  };

  const drivingTime = {
    labels: commonLabels,
    datasets: [
      {
        label: "Driving Time Daily (min)",
        data: generateRandomData(selectedDays, 20, 70),
        borderColor: "#ec4899",
        backgroundColor: "rgba(236,72,153,0.2)",
        tension: 0,
        fill: true,
      },
    ],
  };

  const trips = {
    labels: commonLabels,
    datasets: [
      {
        label: "Driving Trips Daily",
        data: generateRandomData(selectedDays, 1, 5),
        borderColor: "#ec4899",
        backgroundColor: "rgba(236,72,153,0.2)",
        tension: 0,
        fill: true,
      },
    ],
  };

  const exportPDF = async () => {
    if (!dashboardRef.current) return;
    const canvas = await html2canvas(dashboardRef.current);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const width = pdf.internal.pageSize.getWidth();
    const height = (canvas.height * width) / canvas.width;
    pdf.addImage(imgData, "PNG", 0, 0, width, height);
    pdf.save("safety-dashboard.pdf");
  };

  return (
    <div className="p-6 space-y-6" ref={dashboardRef}>
      <div className="flex items-center justify-between flex-wrap gap-4">
        {/* <select
          value={selectedDays}
          onChange={(e) => setSelectedDays(Number(e.target.value))}
          className="border border-green-600 text-green-600 px-4 py-2 rounded-md text-sm"
        >
          <option value={7}>Last 7 Days</option>
          <option value={14}>Last 14 Days</option>
          <option value={30}>Last 30 Days</option>
        </select> */}


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



        <button
          onClick={exportPDF}
          className="border-2 px-4 py-2 rounded-md flex items-center space-x-2 text-sm text-gray-600 hover:text-black"
        >
          <span>Export PDF</span>
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {metricsTop.map((m, i) => (
          <div key={i} className="text-center">
            <div className={`text-2xl font-semibold ${m.color || "text-gray-700"}`}>
              {m.value}
            </div>
            <div className="text-sm text-gray-500">{m.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {metricsBottom.map((m, i) => (
          <div key={i} className="text-center">
            <div className="text-lg font-medium text-gray-700">{m.value}</div>
            <div className="text-sm text-gray-500">{m.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-4 border rounded-lg bg-white shadow-sm h-[40rem]">
          <h3 className="text-md font-bold text-gray-500 mb-4">
            Safety Score: 65
          </h3>
          <Radar data={radarData} />
        </div>

        <div className="p-4 border rounded-lg bg-white shadow-sm h-[40rem]">
          <div className="flex space-x-4 mb-4 overflow-auto">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setSelectedTab(tab)}
                className={`px-3 py-1 rounded-full text-sm border whitespace-nowrap ${
                  selectedTab === tab
                    ? "bg-green-100 text-green-600 border-green-300"
                    : "text-gray-600 border-gray-200"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
          <Line data={lineData} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-4 border rounded-lg bg-white shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-4">
            Mileage Daily (mi)
          </h3>
          <Line data={dailyMileage} />
        </div>

        <div className="p-4 border rounded-lg bg-white shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-4">
            Driving Time Daily (min)
          </h3>
          <Line data={drivingTime} />
        </div>

        <div className="p-4 border rounded-lg bg-white shadow-sm lg:col-span-1">
          <h3 className="text-sm font-medium text-gray-500 mb-4">
            Driving Trips Daily
          </h3>
          <Line data={trips} />
        </div>
      </div>
    </div>
  );
};

export default Safety;