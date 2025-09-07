// src/components/ScoreBlock.tsx
import React from 'react';

interface Props {
  label: string;
  value: string;
  color: 'green' | 'red' | 'yellow';
}

const colorMap = {
  green: 'bg-green-100 text-green-700 border-green-400',
  red: 'bg-red-100 text-red-700 border-red-400',
  yellow: 'bg-yellow-100 text-yellow-800 border-yellow-400',
};

const ScoreBlock = ({ label, value, color }: Props) => {
  return (
    <div className={`border rounded px-4 py-2 text-sm font-medium ${colorMap[color]}`}>
      <div className="mb-1">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
};

export default ScoreBlock;
