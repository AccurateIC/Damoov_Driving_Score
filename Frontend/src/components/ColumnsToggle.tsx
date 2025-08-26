interface Props {
  columns?: string[];
  visibleColumns?: string[];
  onToggle: (col: string) => void;
}

const ColumnsToggle: React.FC<Props> = ({
  columns = [],
  visibleColumns = [],
  onToggle,
}) => {
  return (
    <div className="w-64 bg-white shadow-md rounded border p-3 space-y-2 text-sm">
      {columns.map((col, i) => (
        <label
          key={i}
          className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 px-2 py-1 rounded"
        >
          <input
            type="checkbox"
            checked={visibleColumns.includes(col)}
            onChange={() => onToggle(col)}
            className="accent-green-500"
          />
          {col}
        </label>
      ))}
    </div>
  );
};

export default ColumnsToggle;
