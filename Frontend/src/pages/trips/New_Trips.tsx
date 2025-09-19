// Trips.tsx
import React, { useMemo, useState } from "react";
import { FaDownload, FaSearch, FaUserAlt } from "react-icons/fa";
import { Link } from "react-router-dom"; 

const Trips: React.FC = () => {
  const [trips] = useState([
    {
      id: 1,
      deviceId: "7123456798986981696",
      name: "Name A",
      startTime: "22.8.25 / 4.53 PM",
      endTime: "22.8.25 / 5.53 PM",
      tripDistance: 1,
      uniqueId: 1,
    },
    {
      id: 2,
      deviceId: "8123456798986981697",
      name: "Name B",
      startTime: "22.8.25 / 6.00 PM",
      endTime: "22.8.25 / 7.15 PM",
      tripDistance: 50,
      uniqueId: 50,
    },
    {
      id: 3,
      deviceId: "9123456798986981698",
      name: "Name C",
      startTime: "22.8.26 / 8.30 AM",
      endTime: "22.8.26 / 9.45 AM",
      tripDistance: 40,
      uniqueId: 40,
    },
    {
      id: 4,
      deviceId: "1023456798986981699",
      name: "Name D",
      startTime: "22.8.26 / 10.00 AM",
      endTime: "22.8.26 / 11.20 AM",
      tripDistance: 60,
      uniqueId: 60,
    },
    {
      id: 5,
      deviceId: "1123456798986981700",
      name: "Name E",
      startTime: "22.8.26 / 12.00 PM",
      endTime: "22.8.26 / 1.15 PM",
      tripDistance: 45,
      uniqueId: 45,
    },
    {
      id: 6,
      deviceId: "1223456798986981701",
      name: "Name F",
      startTime: "22.8.26 / 2.00 PM",
      endTime: "22.8.26 / 3.15 PM",
      tripDistance: 30,
      uniqueId: 30,
    },
    {
      id: 7,
      deviceId: "1323456798986981702",
      name: "Name G",
      startTime: "22.8.26 / 4.00 PM",
      endTime: "22.8.26 / 5.15 PM",
      tripDistance: 55,
      uniqueId: 55,
    },
    {
      id: 8,
      deviceId: "1423456798986981703",
      name: "Name H",
      startTime: "22.8.26 / 6.00 PM",
      endTime: "22.8.26 / 7.30 PM",
      tripDistance: 70,
      uniqueId: 70,
    },
    {
      id: 9,
      deviceId: "1523456798986981704",
      name: "Name I",
      startTime: "22.8.26 / 8.00 PM",
      endTime: "22.8.26 / 9.10 PM",
      tripDistance: 25,
      uniqueId: 25,
    },
    {
      id: 10,
      deviceId: "1623456798986981705",
      name: "Name J",
      startTime: "22.8.27 / 9.00 AM",
      endTime: "22.8.27 / 10.30 AM",
      tripDistance: 80,
      uniqueId: 80,
    },
  ]);

  const [searchTerm, setSearchTerm] = useState("");

  const filteredTrips = useMemo(() => {
    const q = searchTerm.trim().toLowerCase();
    if (!q) return trips;
    return trips.filter((t) =>
      Object.values(t).some((val) =>
        val.toString().toLowerCase().includes(q)
      )
    );
  }, [searchTerm, trips]);

  return (
    <div className="p-6 lg:p-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Trips</h2>

        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 border rounded-md px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition">
            <FaDownload className="w-4 h-4" />
            Export as PDF
          </button>

          <select className="border rounded-md px-3 py-1.5 text-sm text-gray-700 hover:border-gray-400">
            <option>Last Year</option>
            <option>Last Month</option>
            <option>Last Week</option>
          </select>
        </div>
      </div>

      <div className="relative mb-4">
        <FaSearch className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
        <input
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by Trip Id, Name, Date, etc."
          className="w-full rounded-full border py-1.5 pl-9 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
      </div>

      <div className="bg-white rounded-xl shadow p-4 overflow-x-auto">
        <table
          className="min-w-full text-sm text-left text-gray-700 border-separate"
          style={{ borderSpacing: "8px 4px" }}
        >
          <thead>
            <tr>
              {["#", "Device ID", "Name", "Start Time", "End Time", "Trip Distance", "Unique ID"].map(
                (el, index) => (
                  <th
                    key={index}
                    className="border-b border-white py-3 px-6 text-center shadow-[0_2px_6px_rgba(0,0,0,0.1)] bg-[#A5B4FC] text-black font-semibold rounded-md"
                  >
                    {el}
                  </th>
                )
              )}
            </tr>
          </thead>

          <tbody>
            {filteredTrips.length > 0 ? (
              filteredTrips.map((trip, idx) => (
                <tr key={trip.id} className="align-middle">
                  <td className="px-3 py-1.5 text-center font-medium">{idx + 1}</td>

                  <td className="px-3 py-1.5 text-center font-medium text-indigo-600 underline">
                    <Link to={`/trips/${trip.deviceId}`}>
                      {trip.deviceId}
                    </Link>
                  </td>                

                  <td className="px-3 py-1.5">
                    <div className="flex items-center justify-center gap-2">
                      <span className="w-7 h-7 rounded-full bg-[#EFEAFB] text-[#6A56F1] flex items-center justify-center text-[10px] shadow-sm">
                        <FaUserAlt className="w-3 h-3" />
                      </span>
                      <span className="font-medium text-sm">{trip.name}</span>
                    </div>
                  </td>

                  <td className="px-3 py-1.5 font-medium text-center">{trip.startTime}</td>
                  <td className="px-3 py-1.5 font-medium text-center">{trip.endTime}</td>
                  <td className="px-3 py-1.5 font-medium text-center">{trip.tripDistance}</td>
                  <td className="px-3 py-1.5 font-medium text-center">{trip.uniqueId}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="px-4 py-6 text-center text-gray-500">
                  No results found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Trips;