// Trips.tsx
import React, { useEffect, useState } from "react";
import { FiSearch, FiDownload } from "react-icons/fi";
import { Link as RouterLink } from "react-router-dom";

const baseURL = import.meta.env.VITE_BASE_URL ;
interface Trip {
  device_id: string;
  start_time: string;
  end_time: string;
  trip_distance_used: number | null;
  unique_id: number;
  name: string;
}

const Trips: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [timeDuration, setTimeDuration] = useState<string>("all"); // all | last_1_week | last_2_weeks | last_1_month | last_2_months
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch trips from API whenever filter changes
  useEffect(() => {
    const fetchTrips = async () => {
      try {
        setLoading(true);
        const url =
          timeDuration === "all"
            ? `${baseURL}/trips_list`
            : `${baseURL}/trips_list?filter=${timeDuration}`;

        const res = await fetch(url);
        if (!res.ok) throw new Error("Failed to fetch trips");
        const data: Trip[] = await res.json();
        setTrips(data);
      } catch (err) {
        console.error("Error fetching trips:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrips();
  }, [timeDuration]);

  // Search filter
  const filteredTrips = trips.filter(
    (t) =>
      t.device_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.unique_id.toString().includes(searchTerm)
  );

  return (
    <div className="flex flex-col gap-6 2xl:px-8 ">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="text-4xl font-bold">Trips</div>
        <div className="flex 2xl:min-w-[350px] gap-4">
          <button className="flex items-center bg-green-600 text-white h-[50px] px-10 rounded-md hover:bg-green-700">
            <FiDownload className="mr-2" /> Export
          </button>

          {/* Time filter select */}
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

      {/* Table */}
      {/* Table */}
      <div className="p-6 mb-4">
        {loading ? (
          <div className="text-center py-6 text-gray-500">Loading trips...</div>
        ) : filteredTrips.length === 0 ? (
          <div className="text-center py-6 text-gray-500">No trips found</div>
        ) : (
          <div className="overflow-x-auto max-h-[550px] overflow-y-auto rounded-2xl shadow">
            <table className="w-full border-collapse bg-white">
              <thead className="sticky top-0 bg-[#B5B6D5] z-10">
                <tr className="text-gray-700 text-sm">
                  <th className="text-center rounded-tl-lg">Unique ID</th>
                  <th className="px-4 py-3 text-center">Device ID</th>
                  <th className="px-4 py-3 text-center">Name</th>
                  <th className="px-4 py-3 text-center">Start Time</th>
                  <th className="px-4 py-3 text-center">End Time</th>
                  <th className="px-4 py-3 text-center">Distance</th>
                </tr>
              </thead>
              <tbody>
                {filteredTrips.map((trip) => (
                  <tr
                    key={trip.unique_id}
                    className="border-b last:border-none"
                  >
                    <td className="text-center">
                      <RouterLink
                        to={`/trips/${trip.unique_id}`}
                        // to={`/users/${user.user_id}`}
                        className="text-indigo-600 hover:underline"
                      >
                        {trip.unique_id}
                      </RouterLink>
                    </td>
                    <td className="text-center">{trip.device_id}</td>
                    <td className="text-center">{trip.name}</td>
                    <td className="text-center">{trip.start_time}</td>
                    <td className="text-center">{trip.end_time}</td>
                    <td className="text-center">
                      {trip.trip_distance_used
                        ? `${trip.trip_distance_used.toFixed(2)} km`
                        : "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Trips;

// // Trips.tsx
// import React, { useEffect, useMemo, useState } from "react";
// import { FiSearch, FiDownload } from "react-icons/fi";
// import { Link as RouterLink } from "react-router-dom";

// interface Trip {
//   device_id: string;
//   start_time: string; // "2025-08-26 20:43:04"
//   end_time: string;
//   trip_distance_used: number | null;
//   unique_id: number;
// }

// const parseDateTime = (s?: string | null): Date | null => {
//   if (!s) return null;
//   // Expecting "YYYY-MM-DD HH:mm:ss" or similar
//   const m = s
//     .trim()
//     .match(/^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?/);
//   if (!m) return null;
//   const [, year, month, day, hour, minute, second] = m;
//   return new Date(
//     Number(year),
//     Number(month) - 1,
//     Number(day),
//     Number(hour),
//     Number(minute),
//     Number(second ?? "0")
//   );
// };

// const Trips: React.FC = () => {
//   const [searchTerm, setSearchTerm] = useState("");
//   const [timeDuration, setTimeDuration] = useState<string>("all"); // all | last_1_week | last_2_weeks | last_1_month | last_2_months

//   const users = [
//     {
//       user_id: "U001",
//       name: "Ankita Mahajan",
//       safety_score: 92.45,
//       trip_count: 15,
//       status: 1,
//     },
//     {
//       user_id: "U002",
//       name: "Rahul Sharma",
//       safety_score: 78.33,
//       trip_count: 8,
//       status: 0,
//     },
//     {
//       user_id: "U003",
//       name: "Priya Verma",
//       safety_score: 85.12,
//       trip_count: 12,
//       status: 1,
//     },
//   ];

//   return (
//     <div className="flex flex-col gap-6 2xl:px-8 ">
//       {/* Header */}
//       <div className="flex justify-between items-center">
//         <div className="text-4xl font-bold">Trips</div>
//         <div className="flex 2xl:min-w-[350px] gap-4">
//           <button className="flex items-center bg-green-600 text-white h-[50px] px-10 rounded-md hover:bg-green-700">
//             <FiDownload className="mr-2" /> Export
//           </button>

//           {/* Time filter select (bound to timeDuration) */}
//           <select
//             className="border px-1 py-2 rounded-md"
//             value={timeDuration}
//             onChange={(e) => setTimeDuration(e.target.value)}
//           >
//             <option value="all">All</option>
//             <option value="last_1_week">Last 1 Week</option>
//             <option value="last_2_weeks">Last 2 Weeks</option>
//             <option value="last_1_month">Last 1 Month</option>
//             <option value="last_2_months">Last 2 Months</option>
//           </select>
//         </div>
//       </div>

//       {/* Search Bar */}
//       <div className="flex items-center bg-white h-[64px] rounded-4xl px-8 py-2 w-full shadow">
//         <FiSearch className="mr-2 text-gray-500 size-6" />
//         <input
//           type="text"
//           placeholder="Search by Device ID or Unique ID"
//           value={searchTerm}
//           onChange={(e) => setSearchTerm(e.target.value)}
//           className="w-full text-xl outline-none"
//         />
//       </div>

//       {/* Table with scroll */}
//       <div className="p-6 mb-4">
//         <table className="w-full border-collapse bg-white rounded-2xl shadow">
//           <thead>
//             <tr className="text-gray-700 text-sm bg-[#B5B6D5]">
//               <th className="text-center rounded-tl-lg">User ID</th>
//               <th className="px-4 py-3 text-center">Name</th>
//               <th className="text-center">Safety Score</th>
//               <th className="text-center">Trip Count</th>
//               <th className="px-4 py-3 text-center">Status</th>
//               <th className="px-4 py-3 text-center">Actions</th>
//             </tr>
//           </thead>
//           <tbody>
//             {users.map((user) => (
//               <tr key={user.user_id} className="border-b last:border-none">
//                 <td className="text-center">
//                   <RouterLink
//                     to={`/users/${user.user_id}`}
//                     className="text-indigo-600 hover:underline"
//                   >
//                     {user.user_id}
//                   </RouterLink>
//                 </td>
//                 <td className="text-center">{user.name}</td>
//                 <td className="px-4 py-3 text-center">
//                   {user.safety_score.toFixed(2)}
//                 </td>
//                 <td className="px-4 py-3 text-center">{user.trip_count}</td>
//                 <td className="px-4 py-3 text-center">
//                   <div className="px-4 py-3 flex items-center justify-center gap-2 text-center">
//                     <span
//                       className={`h-3 w-3 rounded-full ${
//                         user.status === 1 ? "bg-green-500" : "bg-red-500"
//                       }`}
//                     ></span>
//                     {user.status === 1 ? "Active" : "Inactive"}
//                   </div>
//                 </td>
//                 <td className="px-4 py-3 text-center">
//                   <button className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
//                     Delete
//                   </button>
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// };

// export default Trips;
