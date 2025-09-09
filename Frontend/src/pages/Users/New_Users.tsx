import React, { useEffect, useState } from "react";
import { FiSearch, FiDownload } from "react-icons/fi";
import NoData from "../../assets/no-user-data.png";

const baseURL = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:5000";

const UsersList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchId, setSearchId] = useState("");
  const [statusFilter, setStatusFilter] = useState("all"); // NEW

  // Fetch all users on mount
  const loadUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${baseURL}/users`);
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  // Apply both search + dropdown filter
  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(searchId.toLowerCase()) ||
      user.user_id.toString().includes(searchId);

    const matchesStatus =
      statusFilter === "all"
        ? true
        : statusFilter === "active"
        ? user.status === 1
        : user.status === 0;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="2xl:px-8 min-h-screen text-sm gap-6 flex flex-col ">
      <div className="flex justify-between items-center ">
        <div className=" text-4xl font-bold ">Users </div>
        <div className="flex  2xl:w-[350px] gap-4 ">
          <button className="flex items-center bg-green-600 text-white h-[50px] px-10  rounded-md hover:bg-green-700">
            <FiDownload className="mr-2 " /> Export
          </button>

          {/* Dropdown */}
          <select
            className="border px-10 py-2 rounded-md "
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      {/* Search */}
      <div className="flex items-center bg-white h-[64px]  rounded-4xl px-8 py-2 w-full ">
        <FiSearch className="mr-2 text-gray-500 size-6" />
        <input
          type="text"
          placeholder="Search by User ID or Name"
          value={searchId}
          onChange={(e) => setSearchId(e.target.value)}
          className="w-full text-xl outline-none"
        />
      </div>

      {/* Users Table */}
      <div className=" p-6 md:-w-[100px] mb-4">
        {filteredUsers.length > 0 ?  (
          // <table className="mt-4 border bg-white border-gray-300 w-full mt-12 ">
          <table className="w-full border-collapse bg-white rounded-2xl shadow ">
            <thead className="">
              <tr className=" text-gray-700 text-sm">
                <th className=" text-center rounded-tl-lg">User ID</th>
                <th className="px-4 py-3 text-center">Name</th>
                <th className=" text-center">Safety Score</th>
                <th className="text-center">Trip Count</th>
                <th className="px-4 py-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <tr key={user.user_id} className="border-b last:border-none ">
                  <td className="text-center">{user.user_id}</td>
                  <td className="text-center">{user.name}</td>
                  <td className="px-4 py-3  gap-2 text-center">
                    {user.safety_score.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-center">{user.trip_count}</td>
                  <td className="px-4 py-3 text-center">
                    <div className="px-4 py-3 flex items-center justify-center gap-2 text-center">
                      <span
                        className={`h-3 w-3 rounded-full ${
                          user.status === 1 ? "bg-green-500" : "bg-red-500"
                        }`}
                      ></span>
                      {user.status === 1 ? "Active" : "Inactive"}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ): (
    <div className="flex flex-col items-center justify-center mt-12">
      <img
        src={NoData}
        alt="No Data Found"
        className="w-1/5 mb-4"
      />
      <h2 className="text-xl font-semibold text-gray-700">
        No User Found :
      </h2>
      <p className="text-gray-500">
      </p>
    </div>
    )}
      </div>
    </div>
  );
};

export default UsersList;
