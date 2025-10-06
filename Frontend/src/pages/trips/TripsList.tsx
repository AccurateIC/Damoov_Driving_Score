import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiSearch } from "react-icons/fi";

const baseURL = import.meta.env.VITE_BASE_URL;

const TripsList: React.FC = () => {
  const navigate = useNavigate();
  const [searchId, setSearchId] = useState("");
  const [trips, setTrips] = useState<any[]>([]);
  const [searchResult, setSearchResult] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);

  // Load all trips on mount
  useEffect(() => {
    loadTrips();
  }, []);

  const loadTrips = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${baseURL}/trips`);
      const data = await res.json();
      setTrips(data);
    } catch (err) {
      console.error("Error fetching trips:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchId) return;
    setSearchLoading(true);
    try {
      const res = await fetch(`${baseURL}/trips/${searchId}`);
      const data = await res.json();
      setSearchResult(data ? [data] : []);
    } catch (err) {
      console.error("Error searching trip:", err);
      setSearchResult([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const resetSearch = () => {
    setSearchId("");
    setSearchResult([]);
  };

  return (
    <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
      <div className="p-4">
        {/* Load Trips Button */}
        <button
          onClick={loadTrips}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-4"
        >
          {loading ? "Loading..." : "Trips List"}
        </button>

        {/* Search Row */}
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
            <FiSearch className="mr-2 text-gray-500" />
            <input
              type="text"
              placeholder="Search trips by Unique ID"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="w-full text-sm outline-none"
            />
          </div>
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-4 py-2 rounded-md"
          >
            {searchLoading ? "Searching..." : "Search"}
          </button>
          <button
            onClick={resetSearch}
            className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md"
          >
            Reset
          </button>
        </div>

        {/* Search Result Table */}
        {searchResult.length > 0 && (
          <div className="mb-4">
            <h2 className="font-semibold text-gray-700 mb-2">Search Result</h2>
            <table className="w-full border border-gray-300">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border p-2">Unique ID</th>
                  <th className="border p-2">Device ID</th>
                  <th className="border p-2">Start Time</th>
                  <th className="border p-2">End Time</th>
                </tr>
              </thead>
              <tbody>
                {searchResult.map((trip) => (
                  <tr key={trip.unique_id}>
                    <td
                      className="border p-2 text-blue-600 cursor-pointer hover:underline text-center"
                      onClick={() =>
                        navigate(`/dashboard/tripdetails/${trip.unique_id}`)
                      }
                    >
                      {trip.unique_id}
                    </td>
                    <td className="border p-2 text-center">{trip.device_id}</td>
                    <td className="border p-2 text-center">{trip.start_time}</td>
                    <td className="border p-2 text-center">{trip.end_time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* All Trips Table */}
        {trips.length > 0 && (
          <div>
            <h2 className="font-semibold text-gray-700 mb-2">All Trips</h2>
            <table className="w-full border border-gray-300">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border p-2">Unique ID</th>
                  <th className="border p-2">Device ID</th>
                  <th className="border p-2">Start Time</th>
                  <th className="border p-2">End Time</th>
                  <th className="border p-2">Trip Distance</th>
                </tr>
              </thead>
              <tbody>
                {trips.map((trip) => (
                  <tr key={trip.unique_id}>
                    <td
                      className="border p-2 text-blue-600 cursor-pointer hover:underline text-center"
                      onClick={() =>
                        navigate(`/dashboard/tripdetails/${trip.unique_id}`)
                      }
                    >
                      {trip.unique_id}
                    </td>
                    <td className="border p-2 text-center">{trip.device_id}</td>
                    <td className="border p-2 text-center">{trip.start_time}</td>
                    <td className="border p-2 text-center">{trip.end_time}</td>
                    <td className="border p-2 text-center">
                      {trip.trip_distance_used ?? "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {trips.length === 0 && !loading && (
          <div className="text-gray-500 mt-4 text-center">No trips found.</div>
        )}
      </div>
    </div>
  );
};

export default TripsList;
