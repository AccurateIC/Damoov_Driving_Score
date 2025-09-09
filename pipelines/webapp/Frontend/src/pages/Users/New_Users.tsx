// // // // import React, { useState } from "react";
// // // // // import { Button } from "@/components/ui/button"; // shadcn/ui button (if you're using it)
// // // // import { Download, ChevronDown } from "lucide-react"; // icons

// // // // interface User {
// // // //   id: number;
// // // //   userId: string;
// // // //   name: string;
// // // //   tripCount: number;
// // // //   score: number;
// // // //   status: boolean;
// // // // }

// // // // const UsersList: React.FC = () => {
// // // //     const [filter, setFilter] = useState("last_1_month");
// // // //   const [users] = useState<User[]>([
// // // //     { id: 1, userId: "ABCDEFG1234", name: "Name", tripCount: 100, score: 40, status: true },
// // // //     { id: 2, userId: "ABCDEFG1235", name: "Name", tripCount: 230, score: 50, status: true },
// // // //     { id: 3, userId: "ABCDEFG1236", name: "Name", tripCount: 300, score: 40, status: true },
// // // //     { id: 4, userId: "ABCDEFG1237", name: "Name", tripCount: 350, score: 40, status: true },
// // // //     { id: 5, userId: "ABCDEFG1238", name: "Name", tripCount: 400, score: 60, status: true },
// // // //     { id: 6, userId: "ABCDEFG1239", name: "Name", tripCount: 450, score: 60, status: true },
// // // //     { id: 7, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //     { id: 8, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //     { id: 9, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //     { id: 10, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //     { id: 11, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //     { id: 12, userId: "ABCDEFG123", name: "Name", tripCount: 500, score: 45, status: true },
// // // //   ]);

// // // //   return (
// // // //     <div className="px-12">
// // // //       {/* Header */}
// // // //       <div className="flex justify-between  items-center mb-6">
        
// // // //         <h1 className="text-xl font-semibold text-gray-800">Users</h1>
// // // //         {/* <div className="flex gap-3">
// // // //           <Button variant="outline" className="flex items-center gap-2">
// // // //             <Download size={16} /> Export as PDF
// // // //           </Button>
// // // //           <Button variant="outline" className="flex items-center gap-2">
// // // //             Last Year <ChevronDown size={16} />
// // // //           </Button>
// // // //         </div> */}

// // // //            <div className="flex gap-2">
// // // //           <button className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300">
// // // //             Export as PDF
// // // //           </button>
// // // //           {/* <select className="px-3 py-2 border rounded-md bg-amber-500">
// // // //             <option>Last Year</option>
// // // //             <option>Last Month</option>
// // // //             <option>Last Week</option>
// // // //           </select> */}
// // // //            <select
// // // //         className="px-3 py-2 border rounded-md "
// // // //         value={filter}
// // // //         onChange={(e) => setFilter(e.target.value)}
// // // //       >
// // // //         <option value="last_1_week">Last Week</option>
// // // //         <option value="last_2_weeks">Last 2 Weeks</option>
// // // //         <option value="last_1_month">Last Month</option>
// // // //         <option value="last_2_months">Last 2 Months</option>
// // // //       </select>
// // // //         </div>
// // // //       </div>

// // // //       {/* Search Bar */}
// // // //       <input
// // // //         type="text"
// // // //         placeholder="Search by Trip Id, Name, Date, etc."
// // // //         className="w-full mb-6 p-2 border border-gray-300 rounded-lg text-sm focus:outline-none  focus:ring-2 focus:ring-indigo-500"
// // // //       />

// // // //       {/* Table */}
// // // //       <div className="overflow-x-auto rounded-lg shadow bg-white">
// // // //         <table className="min-w-full bg-">
// // // //           <thead>
// // // //             <tr className="bg-gray-100 text-gray-700 text-sm ">
// // // //               <th className="p-3 text-left">#</th>
// // // //               <th className="p-3 text-left">User ID</th>
// // // //               <th className="p-3 text-left">Name</th>
// // // //               <th className="p-3 text-left">Trip Count</th>
// // // //               <th className="p-3 text-left">Score</th>
// // // //               <th className="p-3 text-left">Status</th>
// // // //             </tr>
// // // //           </thead>
// // // //           <tbody>
// // // //             {users.map((u, idx) => (
// // // //               <tr key={u.id} className=" text-sm hover:bg-gray-50">
// // // //                 <td className="p-3">{idx + 1}</td>
// // // //                 <td className="p-3">{u.userId}</td>
// // // //                 <td className="p-3 flex items-center gap-2">
// // // //                   <span className="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center">
// // // //                     👤
// // // //                   </span>
// // // //                   {u.name}
// // // //                 </td>
// // // //                 <td className="p-3">{u.tripCount}</td>
// // // //                 <td className="p-3">{u.score}</td>
// // // //                 <td className="p-3">
// // // //                   <span
// // // //                     className={`w-3 h-3 rounded-full inline-block ${
// // // //                       u.status ? "bg-green-500" : "bg-red-500"
// // // //                     }`}
// // // //                   />
// // // //                 </td>
// // // //               </tr>
// // // //             ))}
// // // //           </tbody>
// // // //         </table>
// // // //       </div>
// // // //     </div>
// // // //   );
// // // // };

// // // // export default UsersList;


// // // import React, { useEffect, useState } from "react";
// // // import { FiSearch } from "react-icons/fi";

// // // const UsersList = () => {
// // //   const [users, setUsers] = useState([]);
// // //   const [loading, setLoading] = useState(false);
// // //   const [searchId, setSearchId] = useState("");

// // //   // Fetch all users
// // //   const loadUsers = async () => {
// // //     setLoading(true);
// // //     try {
// // //       const response = await fetch("http://127.0.0.1:5000/users");
// // //       const data = await response.json();
// // //       setUsers(data);
// // //     } catch (error) {
// // //       console.error("Error fetching users:", error);
// // //     } finally {
// // //       setLoading(false);
// // //     }
// // //   };

// // //   useEffect(() => {
// // //     loadUsers();
// // //   }, []);

// // //   // Filter by search (user_id or name)
// // //   const filteredUsers = users.filter(
// // //     (user) =>
// // //       user.name.toLowerCase().includes(searchId.toLowerCase()) ||
// // //       user.user_id.toString().includes(searchId)
// // //   );

// // //   return (
// // //     <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
// // //       <div className="p-4">
// // //         {/* Load Users Button */}
// // //         <button
// // //           onClick={loadUsers}
// // //           className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
// // //         >
// // //           {loading ? "Loading..." : "Users List"}
// // //         </button>

// // //         {/* Search Row */}
// // //         <div className="flex flex-wrap items-center gap-3 mb-4 mt-4">
// // //           <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
// // //             <FiSearch className="mr-2 text-gray-500" />
// // //             <input
// // //               type="text"
// // //               placeholder="Search by User ID or Name"
// // //               value={searchId}
// // //               onChange={(e) => setSearchId(e.target.value)}
// // //               className="w-full text-sm outline-none"
// // //             />
// // //           </div>
// // //         </div>

// // //         {/* Users Table */}
// // //         {filteredUsers.length > 0 && (
// // //           <table className="mt-4 border border-gray-300 w-full">
// // //             <thead className="bg-gray-200">
// // //               <tr>
// // //                 <th className="border p-2">User ID</th>
// // //                 <th className="border p-2">Name</th>
// // //                 <th className="border p-2">Safety Score</th>
// // //                 <th className="border p-2">Trip Count</th>
// // //                 <th className="border p-2">Status</th>
// // //               </tr>
// // //             </thead>
// // //             <tbody>
// // //               {filteredUsers.map((user) => (
// // //                 <tr key={user.user_id}>
// // //                   <td className="border p-2 text-center">{user.user_id}</td>
// // //                   <td className="border p-2">{user.name}</td>
// // //                   <td className="border p-2 text-center">
// // //                     {user.safety_score.toFixed(2)}
// // //                   </td>
// // //                   <td className="border p-2 text-center">{user.trip_count}</td>
// // //                   <td
// // //                     className={`border p-2 text-center ${
// // //                       user.status === 1 ? "text-green-600" : "text-red-600"
// // //                     }`}
// // //                   >
// // //                     {user.status === 1 ? "Active" : "Inactive"}
// // //                   </td>
// // //                 </tr>
// // //               ))}
// // //             </tbody>
// // //           </table>
// // //         )}
// // //       </div>
// // //     </div>
// // //   );
// // // };

// // // export default UsersList;

// // import React, { useEffect, useState } from "react";
// // import { FiSearch, FiDownload } from "react-icons/fi";

// // const UsersList = () => {
// //   const [users, setUsers] = useState([]);
// //   const [loading, setLoading] = useState(false);
// //   const [searchId, setSearchId] = useState("");

// //   // Fetch all users on mount
// //   const loadUsers = async () => {
// //     setLoading(true);
// //     try {
// //       const response = await fetch("http://127.0.0.1:5000/users");
// //       const data = await response.json();
// //       setUsers(data);
// //     } catch (error) {
// //       console.error("Error fetching users:", error);
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   useEffect(() => {
// //     loadUsers();
// //   }, []);

// //   // Filter by search (user_id or name)
// //   const filteredUsers = users.filter(
// //     (user) =>
// //       user.name.toLowerCase().includes(searchId.toLowerCase()) ||
// //       user.user_id.toString().includes(searchId)
// //   );

// //   return (
// //     <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
// //       <div className="p-4">
// //         {/* Top Bar: Search + Export + Dropdown */}
// //         <div className="flex flex-wrap items-center gap-3 mb-4">
// //           {/* Search */}
// //           <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
// //             <FiSearch className="mr-2 text-gray-500" />
// //             <input
// //               type="text"
// //               placeholder="Search by User ID or Name"
// //               value={searchId}
// //               onChange={(e) => setSearchId(e.target.value)}
// //               className="w-full text-sm outline-none"
// //             />
// //           </div>

// //           {/* Export Button */}
// //           <button className="flex items-center bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
// //             <FiDownload className="mr-2" /> Export
// //           </button>

// //           {/* Dropdown */}
// //           <select className="border px-3 py-2 rounded-md">
// //             <option value="all">All</option>
// //             <option value="active">Active</option>
// //             <option value="inactive">Inactive</option>
// //           </select>
// //         </div>

// //         {/* Users Table */}
// //         {filteredUsers.length > 0 && (
// //           <table className="mt-4 border border-gray-300 w-full">
// //             <thead className="bg-gray-200">
// //               <tr>
// //                 <th className="border p-2">User ID</th>
// //                 <th className="border p-2">Name</th>
// //                 <th className="border p-2">Safety Score</th>
// //                 <th className="border p-2">Trip Count</th>
// //                 <th className="border p-2">Status</th>
// //               </tr>
// //             </thead>
// //             <tbody>
// //               {filteredUsers.map((user) => (
// //                 <tr key={user.user_id}>
// //                   <td className="border p-2 text-center">{user.user_id}</td>
// //                   <td className="border p-2">{user.name}</td>
// //                   <td className="border p-2 text-center">
// //                     {user.safety_score.toFixed(2)}
// //                   </td>
// //                   <td className="border p-2 text-center">{user.trip_count}</td>
// //                   <td
// //                     className={`border p-2 text-center ${
// //                       user.status === 1 ? "text-green-600" : "text-red-600"
// //                     }`}
// //                   >
// //                     {user.status === 1 ? "Active" : "Inactive"}
// //                   </td>
// //                 </tr>
// //               ))}
// //             </tbody>
// //           </table>
// //         )}

// //         {!loading && filteredUsers.length === 0 && (
// //           <p className="mt-4 text-gray-600">No users found.</p>
// //         )}
// //       </div>
// //     </div>
// //   );
// // };

// // export default UsersList;


// import React, { useEffect, useState } from "react";
// import { FiSearch, FiDownload } from "react-icons/fi";

// const UsersList = () => {
//   const [users, setUsers] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [searchId, setSearchId] = useState("");

//   // Fetch all users on mount
//   const loadUsers = async () => {
//     setLoading(true);
//     try {
//       const response = await fetch("http://127.0.0.1:5000/users");
//       const data = await response.json();
//       setUsers(data);
//     } catch (error) {
//       console.error("Error fetching users:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     loadUsers();
//   }, []);

//   // Filter by search (user_id or name)
//   const filteredUsers = users.filter(
//     (user) =>
//       user.name.toLowerCase().includes(searchId.toLowerCase()) ||
//       user.user_id.toString().includes(searchId)
//   );

//   return (
//     <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
//       <div className="p-4">
//         {/* Top Bar: Search + Export + Dropdown */}
//         <div className="flex flex-wrap items-center gap-3 mb-4">
//           {/* Search */}
//           <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
//             <FiSearch className="mr-2 text-gray-500" />
//             <input
//               type="text"
//               placeholder="Search by User ID or Name"
//               value={searchId}
//               onChange={(e) => setSearchId(e.target.value)}
//               className="w-full text-sm outline-none"
//             />
//           </div>

//           {/* Export Button */}
//           <button className="flex items-center bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
//             <FiDownload className="mr-2" /> Export
//           </button>

//           {/* Dropdown */}
//           <select className="border px-3 py-2 rounded-md">
//             <option value="all">All</option>
//             <option value="active">Active</option>
//             <option value="inactive">Inactive</option>
//           </select>
//         </div>

//         {/* Users Table */}
//         {filteredUsers.length > 0 && (
//           <table className="mt-4 border border-gray-300 w-full">
//             <thead className="bg-gray-200">
//               <tr>
//                 <th className="border p-2">User ID</th>
//                 <th className="border p-2">Name</th>
//                 <th className="border p-2">Safety Score</th>
//                 <th className="border p-2">Trip Count</th>
//                 <th className="border p-2">Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {filteredUsers.map((user) => (
//                 <tr key={user.user_id}>
//                   <td className="border p-2 text-center">{user.user_id}</td>
//                   <td className="border p-2">{user.name}</td>
//                   <td className="border p-2 text-center">
//                     {user.safety_score.toFixed(2)}
//                   </td>
//                   <td className="border p-2 text-center">{user.trip_count}</td>
//                   <td className="border p-2 text-center">
//                     <div className="flex items-center justify-center gap-2">
//                       <span
//                         className={`h-3 w-3 rounded-full ${
//                           user.status === 1 ? "bg-green-500" : "bg-red-500"
//                         }`}
//                       ></span>
                   
//                     </div>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         )}

//         {!loading && filteredUsers.length === 0 && (
//           <p className="mt-4 text-gray-600">No users found.</p>
//         )}
//       </div>
//     </div>
//   );
// };

// export default UsersList;


import React, { useEffect, useState } from "react";
import { FiSearch, FiDownload } from "react-icons/fi";


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
    <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
      <div className="p-4">
        {/* Top Bar: Search + Export + Dropdown */}
        <div className="flex flex-wrap items-center gap-3 mb-4">
          {/* Search */}
          <div className="flex items-center bg-white border rounded-md px-3 py-2 w-full md:flex-1">
            <FiSearch className="mr-2 text-gray-500" />
            <input
              type="text"
              placeholder="Search by User ID or Name"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              className="w-full text-sm outline-none"
            />
          </div>

          {/* Export Button */}
          <button className="flex items-center bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
            <FiDownload className="mr-2" /> Export
          </button>

          {/* Dropdown */}
          <select
            className="border px-3 py-2 rounded-md"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        {/* Users Table */}
        {filteredUsers.length > 0 && (
          <table className="mt-4 border border-gray-300 w-full">
            <thead className="bg-gray-200">
              <tr>
                <th className="border p-2">User ID</th>
                <th className="border p-2">Name</th>
                <th className="border p-2">Safety Score</th>
                <th className="border p-2">Trip Count</th>
                <th className="border p-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <tr key={user.user_id}>
                  <td className="border p-2 text-center">{user.user_id}</td>
                  <td className="border p-2">{user.name}</td>
                  <td className="border p-2 text-center">
                    {user.safety_score.toFixed(2)}
                  </td>
                  <td className="border p-2 text-center">{user.trip_count}</td>
                  <td className="border p-2 text-center">
                    <div className="flex items-center justify-center gap-2">
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
        )}

        {!loading && filteredUsers.length === 0 && (
          <p className="mt-4 text-gray-600">No users found.</p>
        )}
      </div>
    </div>
  );
};

export default UsersList;
