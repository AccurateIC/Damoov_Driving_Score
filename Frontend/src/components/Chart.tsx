import React from 'react';
import { Bar, Radar } from 'react-chartjs-2'; 
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  BarElement,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'; 

ChartJS.register(
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  BarElement,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

type ChartType = 'bar' | 'radar';

interface ChartProps {
  type: 'bar' | 'radar';
  title: string;
  labels: string[];
  datasets: any[];
}


const Chart: React.FC<ChartProps> = ({ type, title, labels, datasets }) => {
  const data = {
    labels,
    datasets,
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: title },
    },
  };

  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow p-4">
      {type === 'bar' && <Bar data={data} options={options} />}
      {type === 'radar' && <Radar data={data} options={options} />}
    </div>
  );
};

export default Chart;
