// src/pages/Trips/TimelineChart.tsx
import React from 'react';

const TimelineChart = () => {
  return (
    <div className="space-y-2 text-sm">
      <p className="font-semibold">Phone usage</p>
      <div className="bg-green-200 h-4 rounded w-1/2"></div>
      <p className="font-semibold">Speeding</p>
      <div className="bg-green-400 h-4 rounded w-2/3"></div>
      <p className="font-semibold">Maneuvers</p>
      <div className="bg-green-500 h-4 rounded w-3/4"></div>
      <div className="text-xs text-gray-500">00:00:00 — 04:58:35</div>
    </div>
  );
};

export default TimelineChart;
