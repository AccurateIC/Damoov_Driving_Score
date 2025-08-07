import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { tripsMockData } from '../../data/mockTrips';
import { FiSearch, FiDownload } from 'react-icons/fi';

const TripsList = () => {
  const [searchId, setSearchId] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    const t = tripsMockData.find(t => t.id === searchId.trim());
    if (t) navigate(`/trips/details/${searchId.trim()}`);
    else alert('Trip ID not found!');
  };

  const resetSearch = () => setSearchId('');

  return (
    <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
      <div className="flex gap-4 mb-4">
        <button className="px-4 py-2 bg-green-500 text-white rounded-md">List of Trips</button>
        <button className="px-4 py-2 border rounded-md text-gray-600">Trip Details</button>
      </div>

      <div className="flex flex-wrap items-center gap-3 mb-4">
        <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
          <FiSearch className="mr-2 text-gray-500"/>
          <input
            type="text"
            placeholder="Search trips by ID"
            value={searchId}
            onChange={e => setSearchId(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            className="w-full text-sm outline-none"
          />
        </div>
        <button onClick={resetSearch} className="text-green-600 text-sm underline">Reset</button>
        <button onClick={handleSearch} className="bg-blue-600 text-white px-4 py-2 rounded-md">Search</button>
        <select className="border rounded-md px-3 py-2 bg-white text-sm">
          <option>Last 7 days</option>
          <option>Last 14 days</option>
          <option>Last 30 days</option>
        </select>
        <button className="bg-green-500 text-white px-4 py-2 rounded-md">Add Test Trip(s)</button>
        <input
          placeholder="TrackToken or Track ID"
          className="border px-3 py-2 rounded-md text-sm w-full md:w-64"
        />
      </div>

      <div className="flex items-center justify-between mb-6">
        <button className="bg-green-500 text-white px-4 py-2 rounded-md">Add Filters</button>
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 text-gray-600"><FiDownload /> Export Data</button>
          <button className="border px-4 py-2 bg-white rounded-md text-gray-700">Columns ▾</button>
        </div>
      </div>

      <div className="text-center text-gray-500 mt-32">No results in chosen time period</div>
    </div>
  );
};

export default TripsList;
