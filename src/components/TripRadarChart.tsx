import React from 'react';
import {
  Radar,
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar as RadarChart } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface TripRadarChartProps {
  scores: {
    Phone: number;
    Acceleration: number;
    Brakes: number;
    Cornering: number;
    Speeding: number;
  };
}

const TripRadarChart: React.FC<TripRadarChartProps> = ({ scores }) => {
  const data = {
    labels: ['Phone usage', 'Acceleration', 'Brakes', 'Cornering', 'Speeding'],
    datasets: [
      {
        label: 'Driving Behavior',
        data: [
          scores.Phone,
          scores.Acceleration,
          scores.Brakes,
          scores.Cornering,
          scores.Speeding,
        ],
        backgroundColor: 'rgba(34,197,94,0.2)', // green-500
        borderColor: 'rgba(34,197,94,1)',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      r: {
        angleLines: { display: false },
        suggestedMin: 0,
        suggestedMax: 100,
        ticks: { stepSize: 20 },
        pointLabels: {
          font: { size: 12 },
        },
      },
    },
  };

  return (
    <div className="bg-white shadow rounded p-4">
      <RadarChart data={data} options={options} />
    </div>
  );
};

export default TripRadarChart;
