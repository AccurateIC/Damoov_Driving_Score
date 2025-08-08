// src/components/Card.tsx
import React from 'react';

interface CardProps {
  label: string;
  value: number;
  unit?: string;
}

const Card: React.FC<CardProps> = ({ label, value, unit }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow p-4 flex flex-col justify-between h-full">
      <span className="text-gray-500 text-sm">{label}</span>
      <div className="mt-2 text-2xl font-semibold text-gray-800">
        {value}
        {unit && <span className="text-base text-gray-600 ml-1">{unit}</span>}
      </div>
    </div>
  );
};

export default Card;
