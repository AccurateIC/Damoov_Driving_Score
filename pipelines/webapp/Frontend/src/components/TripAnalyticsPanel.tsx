import React from 'react';

interface TripAnalyticsPanelProps {
  score: number;
  averageSpeed: number;
  maxSpeed: number;
  time: string;
  mileage: string;
  phoneUsageTime: string;
  speedingTime: string;
  accelerations: number;
  brakes: number;
}

const TripAnalyticsPanel: React.FC<TripAnalyticsPanelProps> = ({
  score,
  averageSpeed,
  maxSpeed,
  time,
  mileage,
  phoneUsageTime,
  speedingTime,
  accelerations,
  brakes,
}) => {
  return (
    <div className="bg-white shadow rounded p-4 text-sm grid grid-cols-2 gap-4">
      <div>
        <p className="text-gray-500">Overall Scoring</p>
        <p className="font-semibold text-lg">{score}</p>
      </div>
      <div>
        <p className="text-gray-500">Average Speed</p>
        <p className="font-semibold">{averageSpeed} km/h</p>
      </div>
      <div>
        <p className="text-gray-500">Max Speed</p>
        <p className="font-semibold">{maxSpeed} km/h</p>
      </div>
      <div>
        <p className="text-gray-500">Time</p>
        <p className="font-semibold">{time}</p>
      </div>
      <div>
        <p className="text-gray-500">Mileage</p>
        <p className="font-semibold">{mileage}</p>
      </div>
      <div>
        <p className="text-gray-500">Phone Usage Time</p>
        <p className="font-semibold">{phoneUsageTime}</p>
      </div>
      <div>
        <p className="text-gray-500">Speeding Time</p>
        <p className="font-semibold">{speedingTime}</p>
      </div>
      <div>
        <p className="text-gray-500"># of Accelerations</p>
        <p className="font-semibold">{accelerations}</p>
      </div>
      <div>
        <p className="text-gray-500"># of Brakes</p>
        <p className="font-semibold">{brakes}</p>
      </div>
    </div>
  );
};

export default TripAnalyticsPanel;
