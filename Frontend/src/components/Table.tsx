import React from 'react';

interface Column {
  header: string;
  accessor: string;
}

interface TableProps {
  columns: Column[];
  data: Record<string, any>[];
}

const formatChange = (value: string) => {
  if (!value) return '-';

  const isPositive = value.startsWith('+');
  const isNegative = value.startsWith('-');

  const color = isPositive ? 'text-green-600' : isNegative ? 'text-red-600' : 'text-gray-800';
  const arrow = isPositive ? '▲' : isNegative ? '▼' : '';

  return (
    <span className={`font-medium ${color}`}>
      {arrow} {value.replace(/[+-]/, '')}
    </span>
  );
};

const Table: React.FC<TableProps> = ({ columns, data }) => {
  // Filter out percentage and absolute columns
  const filteredColumns = columns.filter(
    col => col.accessor !== "percentage" && col.accessor !== "absolute"
  );

  return (
    <div className="overflow-x-auto border border-gray-200 rounded-xl bg-white shadow">
      <table className="min-w-full text-sm text-left">
        <thead className="bg-gray-100 text-gray-700">
          <tr>
            {filteredColumns.map((col, idx) => (
              <th key={idx} className="px-4 py-3 font-medium">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rIdx) => (
            <tr key={rIdx} className="border-t hover:bg-gray-50">
              {filteredColumns.map((col, cIdx) => {
                const value = row[col.accessor];
                return (
                  <td key={cIdx} className="px-4 py-2 text-gray-800">
                    {value || "-"}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};


export default Table;
