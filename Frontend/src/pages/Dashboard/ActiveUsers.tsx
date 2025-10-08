import React from "react";
import { useQuery } from "@tanstack/react-query";
import Breadcrumbs from "./Breadcrumbs";

const baseURL = import.meta.env.VITE_BASE_URL;

// API fetch function
const fetchActiveUsers = async (
    
) => {
  const res = await fetch(`${baseURL}/users?filter=last_2_weeks`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
};

const ActiveUsers = () => {
  const { data: users, isLoading, isError, error } = useQuery({
    queryKey: ["active-users", "last_2_weeks"],
    queryFn: fetchActiveUsers,
  });

  if (isLoading) {
    return <p className="p-4">Loading...</p>;
  }

  if (isError) {
    return <p className="p-4 text-red-500">Error: {error.message}</p>;
  }

  return (
    <div className="p-6">
        <div className="p-6">
      <Breadcrumbs />
      <h2 className="text-xl font-semibold mb-4">Active Drivers</h2>
      {/* your table code here */}
    </div>
      <h2 className="text-xl font-bold mb-4 p-4">Active Drivers </h2>
      <table className="w-full border-collapse bg-white rounded-2xl shadow">
        <thead className="">
          <tr className="text-gray-700 text-sm bg-[#B5B6D5]">
            <th className="text-center rounded-tl-lg">User ID</th>
            <th className="px-4 py-3 text-center">Name</th>
            <th className="px-4 py-3 text-center">Safety Score</th>
            <th className="px-4 py-3 text-center">Trip Count</th>
            
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.user_id} className="hover:bg-gray-50 border-b last:border-none">
              <td className="px-4 py-3 gap-2 text-center">{u.user_id}</td>
              <td className="px-4 py-3 gap-2 text-center">{u.name}</td>
              <td className="px-4 py-3 gap-2 text-center">{u.safety_score.toFixed(2)}</td>
              <td className="px-4 py-3 gap-2 text-center">{u.trip_count}</td>
             
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ActiveUsers;
