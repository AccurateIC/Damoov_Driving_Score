import React from "react";

const drivers = [
  { id: 1, token: "ABCDEFG123", name: "Name", distance: 100, score: 40 },
  { id: 2, token: "ABCDEFG123", name: "Name", distance: 230, score: 50 },
  { id: 3, token: "ABCDEFG123", name: "Name", distance: 300, score: 40 },
  { id: 4, token: "ABCDEFG123", name: "Name", distance: 350, score: 40 },
  { id: 5, token: "ABCDEFG123", name: "Name", distance: 400, score: 60 },
  { id: 6, token: "ABCDEFG123", name: "Name", distance: 450, score: 60 },
  { id: 7, token: "ABCDEFG123", name: "Name", distance: 500, score: 45 },
];

const TopDriversTable = ({ top10Aggresive }: { top10Aggresive: string }) => {
  return (
    <div className="bg-white rounded-2xl shadow p-6 md:-w-[100px] mb-4">
      <h2 className="text-gray-800 text-lg font-semibold mb-4">
        {top10Aggresive}
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100 text-gray-700 text-sm">
              <th className="px-4 py-3 text-left rounded-tl-lg">#</th>
              <th className="px-4 py-3 text-left">Driver Token</th>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Distance</th>
              <th className="px-4 py-3 text-left rounded-tr-lg">Score</th>
            </tr>
          </thead>
          <tbody>
            {drivers.map((driver) => (
              <tr
                key={driver.id}
                className="border-b last:border-none text-sm text-gray-700"
              >
                <td className="px-4 py-3">{driver.id}</td>
                <td className="px-4 py-3">{driver.token}</td>
                <td className="px-4 py-3 flex items-center gap-2">
                  <span className="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-500">
                    👤
                  </span>
                  {driver.name}
                </td>
                <td className="px-4 py-3">{driver.distance}</td>
                <td className="px-4 py-3">{driver.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TopDriversTable;
