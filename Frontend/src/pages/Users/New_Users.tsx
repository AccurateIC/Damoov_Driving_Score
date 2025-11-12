import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FiSearch, FiDownload } from "react-icons/fi";
import NoData from "../../assets/no-user-data.png";
import { Link as RouterLink } from "react-router-dom";
import Breadcrumbs from "../Dashboard/Breadcrumbs";

const baseURL = import.meta.env.VITE_BASE_URL;

// Fetch users API
const fetchUsers = async (timeDuration: string) => {
  const res = await fetch(`${baseURL}/users?filter=${timeDuration}`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
};

// Fetch details API (optional)
const fetchUserDetails = async (userId: number) => {
  const res = await fetch(`${baseURL}/user_safety_dashboard_summary?user_id=${userId}`);
  if (!res.ok) throw new Error("Failed to fetch user details");
  return res.json();
};

const UsersList = () => {
  const [searchId, setSearchId] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [timeDuration, setTimeDuration] = useState("last_1_month");

  // Users Query
  const {
    data: users = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["users", timeDuration],
    queryFn: () => fetchUsers(timeDuration),
    staleTime: 1000 * 60 * 5, // cache for 5 minutes
  });

  // Example: Load a fixed user's details
  const { data: detailedUser } = useQuery({
    queryKey: ["userDetails", 11],
    queryFn: () => fetchUserDetails(11),
    staleTime: 1000 * 60 * 10,
  });

  // Filter users
  const filteredUsers = users.filter((user: any) => {
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

  // Delete handler (local only, still can call API if needed)
  const handleDeleteUser = (userId: string) => {
    console.log("Deleting user with ID:", userId);
    // TODO: Call API if backend supports deletion
    // fetch(`${baseURL}/delete_user?user_id=${userId}`, { method: "DELETE" })

    // Local remove
    // Since we're using React Query, we should update cache instead of state
    // We'll do it with queryClient.setQueryData inside a mutation if needed
  };

  if (isLoading) {
    return <div className="text-center py-10 text-gray-600">Loading users...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-10 text-red-600">
        Failed to load users. Please try again later.
      </div>
    );
  }

  return (
    <div className="2xl:px-8 min-h-screen text-sm gap-6 flex flex-col bg-gray-200 ">
      <div className="flex justify-between items-center">
        <span>
           {/* <Breadcrumbs/>   */}
        </span>
        {/* <div className="text-4xl font-bold">Users</div> */}
        <div className="flex 2xl:min-w-[350px] gap-4">
          <button className="flex items-center bg-green-600 text-white h-[50px] px-10 rounded-md hover:bg-green-700">
            <FiDownload className="mr-2" /> Export
          </button>

          {/* Status Filter */}
          <select
            className="border px-2 py-2 rounded-md"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>

          {/* Time Filter */}
          <select
            className="border px-1 py-2 rounded-md"
            value={timeDuration}
            onChange={(e) => setTimeDuration(e.target.value)}
          >
            <option value="last_1_week">Last Week</option>
            <option value="last_2_weeks">Last 2 Weeks</option>
            <option value="last_1_month">Last Month</option>
            <option value="last_2_months">Last 2 Months</option>
          </select>
        </div>
      </div>

      {/* Search */}
      <div className="flex items-center bg-white h-[64px] rounded-4xl px-8 py-2 w-full">
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
      <div className="p-6 md:-w-[100px] mb-4">
        {filteredUsers.length > 0 ? (
          <table className="w-full border-collapse bg-white rounded-2xl shadow">
            <thead>
              <tr className="text-gray-700 text-sm bg-[#B5B6D5]">
                <th className="text-center rounded-tl-lg">User ID</th>
                <th className="px-4 py-3 text-center">Name</th>
                <th className="text-center">Safety Score</th>
                <th className="text-center">Trip Count</th>
                <th className="px-4 py-3 text-center">Status</th>
                <th className="px-4 py-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user: any) => (
                <tr key={user.user_id} className="border-b last:border-none">
                  <td className="text-center">
                    <RouterLink
                      to={`/dashboard/users/${user.user_id}`}
                      className="text-indigo-600 hover:underline"
                    >
                      {user.user_id}
                    </RouterLink>
                  </td>
                  <td className="text-center">{user.name}</td>
                  <td className="px-4 py-3 gap-2 text-center">
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
                  <td className="px-4 py-3 text-center">
                    <button
                      className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                      onClick={() => handleDeleteUser(user.user_id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="flex flex-col items-center justify-center mt-12">
            <img src={NoData} alt="No Data Found" className="w-1/5 mb-4" />
            <h2 className="text-xl font-semibold text-gray-700">No User Found :</h2>
          </div>
        )}
      </div>
    </div>
  );
};

export default UsersList;


// import React, { useEffect, useState } from "react";
// import { FiSearch, FiDownload } from "react-icons/fi";
// import NoData from "../../assets/no-user-data.png";
// import { Link as RouterLink } from "react-router-dom";

// const baseURL = import.meta.env.VITE_BASE_URL ;

// const UsersList = () => {
//   const [users, setUsers] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [searchId, setSearchId] = useState("");
//   const [statusFilter, setStatusFilter] = useState("all"); // NEW
//   const [timeDuration, setTimeDuration] = useState("last_1_month"); // NEW
//   const [detailedUser, setDetailedUser] = useState(null);

//   const loadUsers = async () => {
//     setLoading(true);
//     try {
//       const response = await fetch(`${baseURL}/users?filter=${timeDuration}`);
//       const data = await response.json();
//       setUsers(data);
//       console.log("timeDuration filter", timeDuration);
//       console.log("/users", users);
//     } catch (error) {
//       console.error("Error fetching users:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const loadUserDetails = async () => {
//     try {
//       const response = await fetch(
//         `${baseURL}/user_safety_dashboard_summary?user_id=11`
//       );
//       const data = await response.json();
//       setDetailedUser(data);
//       console.log("User details loaded [Safety Dashboard]:", data);
//     } catch (error) {
//       console.error("Error fetching user details:", error);
//     }
//   };

//   useEffect(() => {
//     loadUsers();
//     loadUserDetails();
//   }, [timeDuration]);

//   const filteredUsers = users.filter((user) => {
//     const matchesSearch =
//       user.name.toLowerCase().includes(searchId.toLowerCase()) ||
//       user.user_id.toString().includes(searchId);

//     const matchesStatus =
//       statusFilter === "all"
//         ? true
//         : statusFilter === "active"
//         ? user.status === 1
//         : user.status === 0;

//     return matchesSearch && matchesStatus;
//   });

//   const handleDeleteUser = (userId: string) => {
//     console.log("Deleting user with ID:", userId);

//     // Example logic: Call your API to delete user
//     // fetch(`${baseURL}/delete_user?user_id=${userId}`, { method: 'DELETE' })

//     // For now, we can filter out the user locally
//     // setFilteredUsers1((prev) => prev.filter((user) => user.user_id !== userId));
//     setUsers((prev) => prev.filter((user) => user.user_id !== userId));
//   };

//   return (
//     <div className="2xl:px-8 min-h-screen text-sm gap-6 flex flex-col ">
//       <div className="flex justify-between items-center">
//         <div className=" text-4xl font-bold ">Users </div>
//         <div className="flex  2xl:min-w-[350px] gap-4 ">
//           <button className="flex items-center bg-green-600 text-white h-[50px] px-10  rounded-md hover:bg-green-700">
//             <FiDownload className="mr-2 " /> Export
//           </button>

//           {/* Dropdown */}
//           <select
//             className="border px-2 py-2 rounded-md "
//             value={statusFilter}
//             onChange={(e) => setStatusFilter(e.target.value)}
//           >
//             <option value="all">All</option>
//             <option value="active">Active</option>
//             <option value="inactive">Inactive</option>
//           </select>
//           <select
//             className="border px-1 py-2 rounded-md "
//             value={timeDuration}
//             onChange={(e) => setTimeDuration(e.target.value)}
//           >
//             <option value="last_1_week">Last Week</option>
//             <option value="last_2_weeks">LAst 2 Weeks</option>
//             <option value="last_1_month">Last Month</option>
//             <option value="last_2_months">Last 2 Months</option>
//           </select>
//         </div>
//       </div>

//       {/* Search */}
//       <div className="flex items-center bg-white h-[64px]  rounded-4xl px-8 py-2 w-full ">
//         <FiSearch className="mr-2 text-gray-500 size-6" />
//         <input
//           type="text"
//           placeholder="Search by User ID or Name"
//           value={searchId}
//           onChange={(e) => setSearchId(e.target.value)}
//           className="w-full text-xl outline-none"
//         />
//       </div>

//       {/* Users Table */}
//       <div className=" p-6 md:-w-[100px] mb-4">
//         {filteredUsers.length > 0 ? (
//           // <table className="mt-4 border bg-white border-gray-300 w-full mt-12 ">
//           <table className="w-full border-collapse bg-white rounded-2xl shadow ">
//             <thead className="">
//               <tr className=" text-gray-700 text-sm bg-[#B5B6D5]">
//                 <th className=" text-center  rounded-tl-lg">User ID</th>
//                 <th className="px-4 py-3 text-center">Name</th>
//                 <th className=" text-center">Safety Score</th>
//                 <th className="text-center">Trip Count</th>
//                 <th className="px-4 py-3 text-center">Status</th>
//                  <th className="px-4 py-3 text-center">Actions</th>{" "}
//               </tr>
//             </thead>
//             <tbody>
//               {filteredUsers.map((user) => (
//                 <tr key={user.user_id} className="border-b last:border-none ">
//                   {/* <td className="text-center">{user.user_id}</td>
//                    */}
//                   <td className="text-center">
//                     <RouterLink
//                       to={`/dashboard/users/${user.user_id}`}
                      
//                       className="text-indigo-600 hover:underline"
//                     >
//                       {user.user_id}
//                     </RouterLink>
//                   </td>
//                   <td className="text-center">{user.name}</td>

//                   <td className="px-4 py-3  gap-2 text-center">
//                     {user.safety_score.toFixed(2)}
//                   </td>
//                   <td className="px-4 py-3 text-center">{user.trip_count}</td>
//                   <td className="px-4 py-3 text-center">
//                     <div className="px-4 py-3 flex items-center justify-center gap-2 text-center">
//                       <span
//                         className={`h-3 w-3 rounded-full ${
//                           user.status === 1 ? "bg-green-500" : "bg-red-500"
//                         }`}
//                       ></span>
//                       {user.status === 1 ? "Active" : "Inactive"}
//                     </div>
//                   </td>
//                      <td className="px-4 py-3 text-center">
//                     <button
//                       className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
//                       onClick={() => handleDeleteUser(user.user_id)}
//                     >
//                       Delete
//                     </button>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
         
//         ) : (
//           <div className="flex flex-col items-center justify-center mt-12">
//             <img src={NoData} alt="No Data Found" className="w-1/5 mb-4" />
//             <h2 className="text-xl font-semibold text-gray-700">
//               No User Found :
//             </h2>
//             <p className="text-gray-500"></p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default UsersList;
