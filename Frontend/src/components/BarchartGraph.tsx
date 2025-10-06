import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const baseURL = import.meta.env.VITE_BASE_URL;
interface ChartDataset {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: (ctx: any) => string;
    borderRadius: number;
  }[];
}

const BarChartGraph = ({ selectedDays }: { selectedDays: number }) => {
  const [selectedParam, setSelectedParam] = useState<string>("Trips");
  // const [selectedPeriod, setSelectedPeriod] = useState<string>("Last 2 Weeks");

  const [chartDataSets, setChartDataSets] = useState<
    Record<string, ChartDataset>
  >({
    Trips: { labels: [], datasets: [] },
    "Driving time": { labels: [], datasets: [] },
    "Safety score": { labels: [], datasets: [] },
    Acceleration: { labels: [], datasets: [] },
    Braking: { labels: [], datasets: [] },
    Cornering: { labels: [], datasets: [] },
    Speeding: { labels: [], datasets: [] },
    "Phone usage": { labels: [], datasets: [] },
  });

  const filterMap: Record<number, string> = {
    7: "last_1_week",
    14: "last_2_weeks",
    30: "last_1_month",
    60: "last_2_months",
  };

  useEffect(() => {
    fetch(`${baseURL}/summary_graph`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        metric: selectedParam,
        filter_val: filterMap[selectedDays],
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        const { labels, data: values, metric } = data;
        console.log("selectedDays", selectedDays);
        setChartDataSets((prev) => ({
          ...prev,
          [metric]: {
            labels,
            datasets: [
              {
                label: metric,
                data:
                  values?.map((val: number) => (isNaN(val) ? 0 : val)) ?? [],
                backgroundColor: (ctx: any) => {
                  const index = ctx.dataIndex;
                  const lastIndex = values.length - 1;
                  return index === lastIndex
                    ? "#4338CA"
                    : "rgba(105, 118, 235, 0.39)"; // dark blue for latest
                },
                borderRadius: 8,
              },
            ],
          },
        }));
      })
      .catch((err) => console.error("Error fetching chart data:", err));
  }, [selectedParam, selectedDays]);

  const options = {
    responsive: true,
    maintainAspectRatio: false as const,
    plugins: {
      legend: { display: false },
      tooltip: { mode: "index" as const, intersect: false },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 12 } },
      },
      y: {
        grid: { color: "#eee" },
        ticks: { stepSize: 10 },
      },
    },
  };

  return (
    // div className="w-[1081px] h-[482px] rounded-[15px] bg-white shadow p-6 flex flex-col">

    <div
      className=" 
    // 2xl:max-w-[1530px] 
  //  2xl:max-h-[830px]
    2xl:bg-white
    2xl:min-h-[500px]
      2xl:max-w-[1630px]  xl:max-w-[1200px] 2xl:max-h-[990px]  
    rounded-xl  shadow-sm "
    >
      {/* Header */}

      <div className="flex items-center gap-3 text-base font-medium  2xl:max-w-[1500px]   pt-[20px] pb-[5px] pl-[50px]">
        <span className="text-gray-600 text-base font-medium ">
          Performance for
        </span>
        <select
          onChange={(e) => setSelectedParam(e.target.value)}
          value={selectedParam}
          className="border border-gray-300 rounded 2xl:max-w-[158px] text-gray-700 px-3 focus:outline-none p-1"
        >
          {Object.keys(chartDataSets).map((param) => (
            <option key={param} value={param}>
              {param}
            </option>
          ))}
        </select>
      </div>

      {/* <div className=" 2xl:max-w-[1470px]  
      // 2xl:max-h-[830px] 
      2xl:min-h-[380px]
      pl-[45.86px]  ">
        <Bar
          data={chartDataSets[selectedParam]}
          options={{
            responsive: true,
            maintainAspectRatio: false,
          }}
        />
      </div> */}
      <div
  className="2xl:max-w-[1470px] 2xl:min-h-[450px] pl-[45.86px]"
>
  <Bar
    data={chartDataSets[selectedParam]}
    options={options}
  />
</div>
    </div>
  );
};

export default BarChartGraph;
