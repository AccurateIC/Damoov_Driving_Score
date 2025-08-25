import React, { useEffect, useState } from "react";
import {
  BarChart,
  ResponsiveContainer,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

export default function Dashboard({ selectedDays }: { selectedDays: number }) {
  const [distributionChart, setDistributionChart] = useState<any>(null);

  const filterMap: Record<number, string> = {
 
  7: "last_1_week",
  14: "last_2_weeks",
  30: "last_1_month",
  60: "last_2_months",
};
 
  const [driverData, setDriverData] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/driver_distribution", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filter_val: filterMap[selectedDays], }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Driver didtribution data:", data);
console.log("selectedDays",selectedDays);
        // ✅ Transform API -> Chart format
        const formatted = data.labels.map((label: string, idx: number) => {
          const value = data.data[idx];

          let safe = 0,
            moderate = 0,
            aggressive = 0;

          if (parseFloat(label) < 70 || label.includes("<")) {
            safe = value;
          } else if (parseFloat(label) >= 70 && parseFloat(label) <= 85) {
            moderate = value;
          } else {
            aggressive = value;
          }

          return {
            range: label,
            Safe: safe,
            Moderate: moderate,
            Aggressive: aggressive,
          };
        });

        setDriverData(formatted);
      })
      .catch((err) => {
        console.error("Error fetching driver distribution:", err);
      });
  }, [selectedDays]);

  const [safetyData, setSafetyData] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/safety_params", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filter_val: filterMap[selectedDays], }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Safety Parma", data);

        // ✅ Convert API response to recharts format
        const formatted = data.labels.map((label: string, idx: number) => ({
          subject: label,
          A: Number(data.data[idx].toFixed(2)), // round to 2 decimals
        }));

        setSafetyData(formatted);
        console.log("safetyData", safetyData);
      })
      .catch((err) => {
        console.error("Error fetching safety params:", err);
      });
  }, [selectedDays]);

  return (
//     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//   {/* Left card - Driver Distribution */}
//   <div className="bg-white rounded-2xl shadow p-6">
//     <div className="flex justify-between items-center mb-4">
//       <h2 className="text-lg font-semibold">Driver Distribution</h2>
//     </div>

//     <ResponsiveContainer width="100%" height={400}>
//       <BarChart data={driverData} layout="vertical" margin={{ left: 40 }}>
//         <XAxis type="number" />
//         <YAxis dataKey="range" type="category" />
//         <Tooltip />
//         <Legend />
//         <Bar dataKey="Safe" fill="#4fd1c5" barSize={20} />
//         <Bar dataKey="Moderate" fill="#b7791f" barSize={20} />
//         <Bar dataKey="Aggressive" fill="#e53e3e" barSize={20} />
//       </BarChart>
//     </ResponsiveContainer>
//   </div>

//   {/* Right card - Safety Parameters */}
//   <div className="bg-white rounded-2xl shadow p-6 flex flex-col">
//     <h2 className="text-lg font-semibold mb-4">Safety Parameters</h2>

//     <div className="flex justify-center">
//       <RadarChart
//         cx={150}
//         cy={120}
//         outerRadius={80}
//         width={260}
//         height={220}
//         data={safetyData}
//       >
//         <PolarGrid />
//         <PolarAngleAxis dataKey="subject" />
//         <PolarRadiusAxis angle={30} domain={[0, 1000]} />
//         <Radar
//           name="Score"
//           dataKey="A"
//           stroke="#4f46e5"
//           fill="#6366f1"
//           fillOpacity={0.6}
//         />
//       </RadarChart>
//     </div>

//     <div className="mt-4 space-y-2">
//       {safetyData.map((item, idx) => (
//         <div
//           key={idx}
//           className="flex justify-between items-center border-b pb-1"
//         >
//           <span className="text-gray-700">{item.subject}</span>
//           <span className="text-indigo-600 font-semibold">{item.A}</span>
//         </div>
//       ))}
//     </div>
//   </div>
// </div>

<div className="flex flex-col md:flex-row gap-6">
  {/* Left card - Driver Distribution */}
  <div className="bg-white rounded-2xl md:w-[1060px] shadow p-6 ">
    <div className="flex justify-between items-center mb-4">
      <h2 className="text-lg font-semibold">Driver Distribution</h2>
    </div>

    <ResponsiveContainer height={400}>
      <BarChart data={driverData} layout="vertical" margin={{ left: 40 }}>
        <XAxis type="number" />
        <YAxis dataKey="range" type="category" />
        <Tooltip />
        <Legend />
        <Bar dataKey="Safe" fill="#4fd1c5" barSize={20} />
        <Bar dataKey="Moderate" fill="#b7791f" barSize={20} />
        <Bar dataKey="Aggressive" fill="#e53e3e" barSize={20} />
      </BarChart>
    </ResponsiveContainer>
  </div>

  {/* Right card - Safety Parameters */}
  <div className="bg-white rounded-2xl shadow p-6 flex flex-col md:w-[410px]">
    <h2 className="text-lg font-semibold mb-4">Safety Parameters</h2>

    <div className="flex justify-center">
      <RadarChart
        cx={150}
        cy={120}
        outerRadius={80}
        width={260}
        height={220}
        data={safetyData}
      >
        <PolarGrid />
        <PolarAngleAxis dataKey="subject" />
        <PolarRadiusAxis angle={30} domain={[0, 100]} />
        <Radar
          name="Score"
          dataKey="A"
          stroke="#4f46e5"
          fill="#6366f1"
          fillOpacity={0.6}
        />
      </RadarChart>
    </div>

    <div className="mt-4 space-y-2">
      {safetyData.map((item, idx) => (
        <div
          key={idx}
          className="flex justify-between items-center border-b pb-1"
        >
          <span className="text-gray-700">{item.subject}</span>
          <span className="text-indigo-600 font-semibold">{item.A}</span>
        </div>
      ))}
    </div>
  </div>
</div>

);
}
