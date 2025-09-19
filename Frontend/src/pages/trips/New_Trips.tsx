// Trips.tsx
import React, { useEffect, useMemo, useState } from "react";
import { FiSearch, FiDownload } from "react-icons/fi";
import { Link } from "react-router-dom";

interface Trip {
  device_id: string;
  start_time: string; // "2025-08-26 20:43:04"
  end_time: string;
  trip_distance_used: number | null;
  unique_id: number;
}

const parseDateTime = (s?: string | null): Date | null => {
  if (!s) return null;
  // Expecting "YYYY-MM-DD HH:mm:ss" or similar
  const m = s
    .trim()
    .match(/^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?/);
  if (!m) return null;
  const [, year, month, day, hour, minute, second] = m;
  return new Date(
    Number(year),
    Number(month) - 1,
    Number(day),
    Number(hour),
    Number(minute),
    Number(second ?? "0")
  );
};

const Trips: React.FC = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [timeDuration, setTimeDuration] = useState<string>("all"); // all | last_1_week | last_2_weeks | last_1_month | last_2_months

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/trips");
        const data = await res.json();
        setTrips(data);
      } catch (error) {
        console.error("Error fetching trips:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTrips();
  }, []);

  // compute start date for time filter
  const getFromDate = (duration: string): Date | null => {
    if (!duration || duration === "all") return null;
    const now = new Date();
    const daysMap: Record<string, number> = {
      last_1_week: 7,
      last_2_weeks: 14,
      last_1_month: 30,
      last_2_months: 60,
    };
    const days = daysMap[duration] ?? 0;
    if (!days) return null;
    const from = new Date(now);
    from.setDate(now.getDate() - days);
    return from;
  };

  // Search + Time filter combined
  const filteredTrips = useMemo(() => {
    const q = searchTerm.trim().toLowerCase();
    const fromDate = getFromDate(timeDuration);
    const now = new Date();

    return trips.filter((t) => {
      // 1) Search filter (device_id or unique_id)
      if (q) {
        const matchesSearch =
          t.device_id?.toLowerCase().includes(q) ||
          t.unique_id?.toString().toLowerCase().includes(q);
        if (!matchesSearch) return false;
      }

      // 2) Time filter (compare start_time)
      if (fromDate) {
        const start = parseDateTime(t.start_time);
        if (!start) return false; // exclude if start_time malformed/missing
        // include only trips whose start_time is between fromDate and now
        if (start < fromDate || start > now) return false;
      }

      return true;
    });
  }, [searchTerm, trips, timeDuration]);

  return (
    <div className="flex flex-col gap-6 2xl:px-8 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="text-4xl font-bold">Trips</div>
        <div className="flex 2xl:min-w-[350px] gap-4">
          <button className="flex items-center bg-green-600 text-white h-[50px] px-10 rounded-md hover:bg-green-700">
            <FiDownload className="mr-2" /> Export
          </button>

          {/* Time filter select (bound to timeDuration) */}
          <select
            className="border px-1 py-2 rounded-md"
            value={timeDuration}
            onChange={(e) => setTimeDuration(e.target.value)}
          >
            <option value="all">All</option>
            <option value="last_1_week">Last 1 Week</option>
            <option value="last_2_weeks">Last 2 Weeks</option>
            <option value="last_1_month">Last 1 Month</option>
            <option value="last_2_months">Last 2 Months</option>
          </select>
        </div>
      </div>

      {/* Search Bar */}
      <div className="flex items-center bg-white h-[64px] rounded-4xl px-8 py-2 w-full shadow">
        <FiSearch className="mr-2 text-gray-500 size-6" />
        <input
          type="text"
          placeholder="Search by Device ID or Unique ID"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full text-xl outline-none"
        />
      </div>

      {/* Table with scroll */}
      <div className="p-4  rounded-2xl shadow mb-4">
        {loading ? (
          <div className="text-center text-gray-500">Loading trips...</div>
        ) : (
          <div className="overflow-x-auto max-h-[500px] overflow-y-auto rounded-lg">
            <table
              className="min-w-full text-sm text-left text-gray-700 border-separate"
              style={{ borderSpacing: "8px 4px" }}
            >
              <thead className="sticky top-0 bg-[#B5B6D5] z-10">
                <tr>
                  {[
                    "#",
                    "Device ID",
                    "Start Time",
                    "End Time",
                    "Trip Distance",
                    "Unique ID",
                  ].map((el, index) => (
                    <th
                      key={index}
                      className="px-4 py-3 text-center font-semibold text-gray-700"
                    >
                      {el}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredTrips.length > 0 ? (
                  filteredTrips.map((trip, idx) => (
                    <tr
                      key={trip.unique_id}
                      className="align-middle hover:bg-gray-100"
                    >
                      <td className="px-3 py-1.5 text-center font-medium">
                        {idx + 1}
                      </td>
                      <td className="px-3 py-1.5 text-center font-medium text-indigo-600 underline">
                        <Link to={`/trips/${trip.device_id}`}>
                          {trip.device_id}
                        </Link>
                      </td>
                      <td className="px-3 py-1.5 font-medium text-center">
                        {trip.start_time}
                      </td>
                      <td className="px-3 py-1.5 font-medium text-center">
                        {trip.end_time}
                      </td>
                      <td className="px-3 py-1.5 font-medium text-center">
                        {trip.trip_distance_used ?? "N/A"}
                      </td>
                      <td className="px-3 py-1.5 font-medium text-center">
                        {trip.unique_id}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-4 py-6 text-center text-gray-500"
                    >
                      No results found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Trips;
