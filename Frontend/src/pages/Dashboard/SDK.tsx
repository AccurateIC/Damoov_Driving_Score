import React, { useState, useMemo } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

const getDummyData = (days: number) => {
  const labels = Array.from({ length: days }, (_, i) => `Jul ${i + 1}`);
  const selectedPeriod = Array.from({ length: days }, (_, i) =>
    Math.floor(Math.random() * 5)
  );
  const previousPeriod = Array.from({ length: days }, () =>
    Math.floor(Math.random() * 2)
  );

  return { labels, selectedPeriod, previousPeriod };
};

const SDK = () => {
  const [period, setPeriod] = useState(7);
  const { labels, selectedPeriod, previousPeriod } = useMemo(
    () => getDummyData(period),
    [period]
  );

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "right" },
    },
    scales: {
      x: { grid: { color: "#eee" } },
      y: { grid: { color: "#eee" } },
    },
  };

  const chartStyle = "h-[320px] bg-white p-4 rounded-xl shadow mb-8";

  const chartData = (label: string) => ({
    labels,
    datasets: [
      {
        label: "Selected Period",
        data: selectedPeriod,
        fill: false,
        borderColor: "#22c55e",
        backgroundColor: "#22c55e",
        tension: 0.3,
      },
      {
        label: "Previous Period",
        data: previousPeriod,
        fill: false,
        borderColor: "#999",
        backgroundColor: "#999",
        borderDash: [4, 4],
        tension: 0.3,
      },
    ],
  });

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-800">
        SDK Dashboard
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 items-center">
        <div className="col-span-2 grid grid-cols-2 gap-6 mb-[5rem]">
          <div className="bg-gray-200 rounded-xl shadow p-4 text-center">
            <p className="text-2xl font-bold text-gray-800">3</p>
            <p className="text-sm text-gray-500">
              Total number of Registrations (incl. deleted)
            </p>
          </div>
          <div className="bg-gray-200 rounded-xl shadow p-4 text-center">
            <p className="text-2xl font-bold text-gray-800">3</p>
            <p className="text-sm text-gray-500">
              Total number of users with trips
            </p>
          </div>
        </div>

        <div className="col-span-1 flex justify-center">
          <div className="relative w-64 h-64">
            <svg className="transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-green-400"
                stroke="currentColor"
                strokeWidth="3"
                fill="none"
                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className="text-green-700"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
                strokeDasharray="100, 100"
                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center text-sm text-gray-700">
              <span className="font-semibold">Registered</span>
              <span className="text-xs">100%</span>
              <span className="text-xs text-gray-400">Active</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-[-5rem]">
        <label className="font-medium text-gray-700 mr-3">Time Period:</label>
        <select
          value={period}
          onChange={(e) => setPeriod(Number(e.target.value))}
          className="border border-green-500 text-green-600 px-3 py-2 rounded-md text-sm font-medium mb-5"
        >
          <option value={7}>Latest 7 Days</option>
          <option value={14}>Latest 14 Days</option>
          <option value={30}>Latest 30 Days</option>
          <option value={60}>Latest 60 Days</option>
        </select>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 items-center">
          <div className="col-span-2 grid grid-cols-2 gap-6">
            <div className="bg-gray-200 rounded-xl shadow p-4 text-center">
              <p className="text-2xl font-bold text-gray-800">3</p>
              <p className="text-sm text-gray-500">
                New registrations in active period (incl.deleted)
              </p>
            </div>
            <div className="bg-gray-200 rounded-xl shadow p-4 text-center">
              <p className="text-2xl font-bold text-gray-800">3</p>
              <p className="text-sm text-gray-500">
                Users with trips within a period{" "}
              </p>
            </div>
          </div>
        </div>

        <div className={chartStyle}>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Accumulated Number of Registered Users
          </h3>
          <Line options={chartOptions} data={chartData("Accumulated Users")} />
        </div>

        <div className={chartStyle}>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Number of Registrations
          </h3>
          <Line options={chartOptions} data={chartData("Registrations")} />
        </div>

        <div className={chartStyle}>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Number of Active Users
          </h3>
          <Line options={chartOptions} data={chartData("Active Users")} />
        </div>
      </div>
    </div>
  );
};

export default SDK;
