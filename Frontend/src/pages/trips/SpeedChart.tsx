// src/pages/Trips/SpeedChart.tsx
import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const SpeedChart = () => {
  const labels = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00'];
  const data = {
    labels,
    datasets: [
      {
        label: 'Speed (km/h)',
        data: [42, 36, 58, 70, 48, 63, 55],
        backgroundColor: (ctx) => {
          const value = ctx.raw;
          return value > 60 ? '#ef4444' : '#22c55e'; // red if > 60 km/h
        },
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Speed (km/h)' },
      },
      x: {
        title: { display: true, text: 'Time' },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.y} km/h`,
        },
      },
    },
  };

  return (
    <div>
      <Bar data={data} options={options} />
      <p className="mt-2 text-sm text-gray-500">
        <span className="text-green-600 font-semibold">Green</span> = Within Limit, &nbsp;
        <span className="text-red-600 font-semibold">Red</span> = Speeding Detected
      </p>
    </div>
  );
};

export default SpeedChart;
