import React, { use, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { tripsMockData } from "../../data/mockTrips";
import { FiSearch, FiDownload } from "react-icons/fi";

const TripsList = () => {
  // const [searchId, setSearchId] = useState('');
  const navigate = useNavigate();
  const [searchId, setSearchId] = useState('');
  const [tripDetails, setTripDetails] = useState([]);

  const handleSearch = () => {
    // Load trips on component mount
    fetch(`http://127.0.0.1:5000/trips/${searchId}`)
      .then((response) => response.json())
      .then((data) => {
        setTripDetails(data);
      })
      .catch((error) => console.error("Error fetching trips:", error));
    console.log("tripDetails", tripDetails);
    // console.log("searchId djh", searchId);
    loadTrips();
  };

  const resetSearch = () => setSearchId("");
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadTrips = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/trips");
      const data = await response.json();
      setTrips(data);
    } catch (error) {
      console.error("Error fetching trips:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
      <div className="p-4">
        {/* Load Trips Button */}
        <button
          onClick={loadTrips}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {loading ? "Loading..." : "Trips List"}
        </button>

        {/* Search Row (Moved Below Button) */}
        <div className="flex flex-wrap items-center gap-3 mb-4 mt-4">
          <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
            <FiSearch className="mr-2 text-gray-500" />
            <input
              type="text"
              placeholder="Search trips by ID"
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
            Search
          </button>
          {tripDetails && Object.keys(tripDetails).length > 0 && (
            <table className="mt-4 border border-gray-300 w-full">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border p-2">Device ID</th>
                  <th className="border p-2">Start Time</th>
                  <th className="border p-2">End Time</th>
                  <th className="border p-2">Unique ID</th>
                </tr>
              </thead>
              <tbody>
                {[tripDetails].map((trip, index) => (
                  <tr key={index}>
                    <td className="border p-2">{trip.device_id}</td>
                    <td className="border p-2">{trip.start_time}</td>
                    <td className="border p-2">{trip.end_time}</td>
                    <td className="border p-2">{trip.unique_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Trips Table */}
        {trips.length > 0 && (
          <table className="mt-4 border border-gray-300 w-full">
            <thead className="bg-gray-200">
              <tr>
                <th className="border p-2">Device ID</th>
                <th className="border p-2">Start Time</th>
                <th className="border p-2">End Time</th>
                <th className="border p-2">Trip Distance Used</th>
                <th className="border p-2">Unique ID</th>
              </tr>
            </thead>
            <tbody>
              {trips.map((trip, index) => (
                <tr key={index}>
                  <td className="border p-2">{trip.device_id}</td>
                  <td className="border p-2">{trip.start_time}</td>
                  <td className="border p-2">{trip.end_time}</td>
                  <td className="border p-2">
                    {trip.trip_distance_used ?? "N/A"}
                  </td>
                  <td className="border p-2">{trip.unique_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default TripsList;
