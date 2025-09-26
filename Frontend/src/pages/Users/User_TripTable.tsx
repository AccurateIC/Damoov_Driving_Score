import React, { useEffect, useState } from "react";

const sampleTrips = Array.from({ length: 10 }, (_, idx) => ({
  deviceId: "12345",
  name: "Trip1",
  startTime: "22.8.25 / 4:53 PM",
  endTime: "22.8.25 / 4:53 PM",
  tripDistance: idx % 5 === 0 ? 1 : 45 + (idx % 3) * 5,
  uniqueId: idx + 1,
}));

type TripsTableProps = {
  userId: string;
  statusFilter: string;
};

type Trip = {
  device_id: string;
  name: string;
  start_time: string;
  end_time: string;
  trip_distance_used: number;
  unique_id: number;
};

const baseURL = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:5000";

const TripsTable = ({ userId, statusFilter }: TripsTableProps) => {
  const [userTrips, setUserTrips] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTrips = async () => {
    setLoading(true);
    setError(null);

    try {
      console.log(
        "Fetching trips for user:",
        userId,
        "with filter:",
        statusFilter
      );
      // ​http://127.0.0.1:5000/user_trips1?user_id=13&filter=last_2_months
      const res = await fetch(
        `${baseURL}/user_trips1?user_id=${userId}&filter=${statusFilter}`
      );

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setUserTrips(data);
      console.log("userTrips fetched:", data);
    } catch (err: any) {
      console.error("Error fetching trips:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrips();
  }, [userId, statusFilter]);

  return (
    <div className="m-2 md:w-full mb-4 ">
      {/* Scroll container */}
      <div className="max-h-[450px] overflow-auto bg-white rounded-lg">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-[#B5B6D5] text-gray-700 sticky top-0">
              <th className="p-2 rounded-tl-lg">#</th>
              <th className="p-2">Device ID</th>
              <th className="p-2">Name</th>
              <th className="p-2">Start Time</th>
              <th className="p-2">End Time</th>
              <th className="p-2">Trip Distance Used</th>
              <th className="p-2">Unique ID</th>
            </tr>
          </thead>

          <tbody>
            {userTrips.length > 0 ? (
              userTrips.map((trip, index) => (
                <tr
                  key={index}
                  className="text-center border-b last:border-none font-md text-[14px] hover:bg-gray-100"
                >
                  <td className="px-4 py-3">{index + 1}</td>
                  <td className="px-4 py-3">{trip.device_id}</td>
                  <td className="px-4 py-3">{trip.name}</td>
                  <td className="px-4 py-3">{trip.start_time}</td>
                  <td className="px-4 py-3">{trip.end_time}</td>
                  <td className="px-4 py-3">{trip.trip_distance_used}</td>
                  <td className="px-4 py-3">{trip.unique_id}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="text-center py-4">
                  Loading.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TripsTable;
