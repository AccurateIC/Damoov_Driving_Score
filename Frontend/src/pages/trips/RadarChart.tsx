// src/pages/Trips/RadarChart.tsx
import React from 'react';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const RadarChart = () => {
  const data = {
    labels: ['Phone usage', 'Acceleration', 'Brakes', 'Cornering', 'Speeding'],
    datasets: [
      {
        label: 'Scoring',
        data: [95, 82, 77, 60, 100],
        backgroundColor: 'rgba(0, 200, 83, 0.3)',
        borderColor: '#00c853',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    scales: {
      r: {
        suggestedMin: 0,
        suggestedMax: 100,
        pointLabels: {
          font: { size: 12 },
          color: '#333',
        },
        ticks: {
          stepSize: 20,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div>
      <Radar data={data} options={options} />
      <div className="mt-4 text-sm">
        <p>📊 <strong>Overall scoring:</strong> 83</p>
        <p>📱 Phone usage: 95</p>
        <p>🚗 Acceleration: 82</p>
        <p>🛑 Brakes: 77</p>
        <p>🌀 Cornering: 60</p>
        <p>⚡ Speeding: 100</p>
        <hr className="my-2" />
        <p>Average speed: 36.66 mi/h</p>
        <p>Maximum speed: 62.14 mi/h</p>
        <p>Time: 298 min</p>
        <p>Mileage: 20.44 mi</p>
      </div>
    </div>
  );
};

export default RadarChart;
