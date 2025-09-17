// // // import React from "react";
// // // import { FiSearch, FiDownload } from "react-icons/fi";
// // // import DeleteIcon from "@mui/icons-material/Delete";
// // // function User_Details() {
// // //   const [statusFilter, setStatusFilter] = React.useState("all"); // NEW
// // //   return (
// // //     <div className="flex flex-col gap-[5px] bg-amber-100 min-h-screen 2xl:min-w-[1081px] 2xl:mx-10">
// // //       <div className="flex justify-between bg-amber-300 items-center ">
// // //         <div className=" text-3xl font-medium ">User Profile </div>
// // //         <div className="flex  2xl:min-w-[350px] gap-4 ">
// // //           <button className="border rounded-md p-2">
// // //             Delete User
// // //             <DeleteIcon />
// // //           </button>
// // //           <button className="flex items-center border h-[50px] px-8  rounded-md hover:bg-green-700">
// // //             Export PDF <FiDownload className="ml-2 " />
// // //           </button>
// // //           <select
// // //             className="border px-10 py-2 rounded-md "
// // //             value={statusFilter}
// // //             onChange={(e) => setStatusFilter(e.target.value)}
// // //           >
// // //             <option value="all">All</option>
// // //             <option value="active">Active</option>
// // //             <option value="inactive">Inactive</option>
// // //           </select>
// // //         </div>
// // //       </div>

// // //       <div className=" bg-amber-600  min-h-screen grid grid-cols-1 gap-10 p-4">
// // //         <div className="grid grid-cols-2 h-[178px] bg-amber-400 gap-10 p-4">
// // //           <div className=" bg-amber-500">hello</div>
// // //           <div className=" bg-amber-500">heelo2</div>
// // //         </div>
// // //         <div className="min-h-screen bg-amber-700">h3</div>
// // //       </div>
// // //     </div>
// // //   );
// // // }

// // // export default User_Details;

// // import React from "react";
// // import { FiDownload } from "react-icons/fi";
// // import DeleteIcon from "@mui/icons-material/Delete";
// // import { Star, AlertCircle } from "lucide-react";
// // import Tabs from "./dummtTab";

// // function User_Details() {
// //   const [statusFilter, setStatusFilter] = React.useState("all"); // NEW

// //   return (
// //     <div className="flex flex-col gap-[5px] min-h-screen 2xl:min-w-[1530px] 2xl:mx-10 pt-[43px]">
// //       {/* Header */}
// //       <div className="flex justify-between  items-center p-1">
// //         <div className=" text-3xl font-medium ">User Profile</div>
// //         <div className="flex 2xl:min-w-[350px] gap-4">
// //           <button className="border rounded-md p-2 flex items-center gap-2">
// //             Delete User
// //             <DeleteIcon />
// //           </button>
// //           <button className="flex items-center border h-[50px] px-8 rounded-md hover:bg-green-700">
// //             Export PDF <FiDownload className="ml-2 " />
// //           </button>
// //           <select
// //             className="border px-10 py-2 rounded-md"
// //             value={statusFilter}
// //             onChange={(e) => setStatusFilter(e.target.value)}
// //           >
// //             <option value="all">Last Week</option>
// //             <option value="Last Week">Last 2 Week</option>
// //             <option value="Last  Month">Last Month</option>
// //            < option value="Last 2 Month">Last 2 Month</option>
// //           </select>
// //         </div>
// //       </div>

// //       <div className=" grid grid-cols-1 p-2 bg-">
// //         <div className="grid grid-cols-1 px-4 2xl:min-h-[200px] ">
// //           <div className="flex items-center  justify-between  rounded-lg  p-2 w-full">
// //             <div className="flex flex-col  items-start  gap-5 h-full pl-4 rounded-lg w-3/5">
// //               <div className="2xl:min-w-[80px] 2xl:min-h-[80px] rounded-full bg-[#A5A6F6] bg- flex items-center justify-center text-white font-bold text-xl">
// //                 <span role="img" aria-label="avatar">
// //                   🧑‍💼
// //                 </span>
// //               </div>
// //               <div className="flex flex-col gap-2">
// //                 <h2 className="font-bold text-2xl">User 1</h2>
// //                 <div className="flex flex-row gap-4">
// //                   {" "}
// //                   <p className="font-[16px] text-gray-500">
// //                     User ID: <span className="text-gray-700">ABCDEF123</span>
// //                   </p>
// //                   <p className="font-[16px] text-gray-500">
// //                     Registration Date:{" "}
// //                     <span className="text-gray-700">10 Sepember 2025</span>
// //                   </p>
// //                 </div>
// //               </div>
// //             </div>
// //             {/* Right Section */}
// //             <div className="h-full pt- pr-6 flex flex-col gap-4 font-medium ">
// //               <div className="w-full text-base font-medium flex items-center gap-2  ">
// //                 <div className="bg-[#484AB8] text-white rounded-full 3xl:min-w-[42px] 3xl:min-h-[42px] flex items-center justify-center  ">
// //                   <Star />
// //                 </div>
// //                 <span className=" text-gray-700">
// //                   #2 driver on the list this week
// //                 </span>
// //               </div>

// //               <div className="flex items-center text-base font-medium gap-2 ">
// //                 <div className="bg-[#484AB8] text-white rounded-full 3xl:min-w-[42px] 3xl:min-h-[42px] flex items-center justify-center ">
// //                   <Star  />
// //                 </div>
// //                 <span className=" text-gray-700">Speed streak day 6</span>
// //               </div>

// //               <div className="flex items-center gap-2 text-base font-medium">
// //                 <div className="bg-[#AF855A] 3xl:min-w-[42px] 3xl:min-h-[42px] text-white rounded-full flex items-center justify-center ">
// //                   <AlertCircle  />
// //                 </div>
// //                 <span className=" text-gray-700">Over speeding sometimes</span>
// //               </div>
// //             </div>
// //           </div>
// //         </div>

// //         {/* Other content */}
// //         <div className="flex flex-col flex-grow  rounded-lg p-2">
// //           <Tabs />
// //         </div>
// //       </div>
// //     </div>
// //   );
// // }

// // export default User_Details;

// import React, { useState } from "react";
// import { FiDownload } from "react-icons/fi";
// import DeleteIcon from "@mui/icons-material/Delete";
// import { Star, AlertCircle } from "lucide-react";
// import TripsTable from "./User_TripTable";

// function UserDetailsWithTabs() {
//   const [statusFilter, setStatusFilter] = useState("all");
//   const [activeTab, setActiveTab] = useState("Safety Parameters");

//   const cards = [
//     { title: "Safety Score", value: "79.81", unit: "mh" },
//     { title: "Trust Level", value: "100", unit: "" },
//     { title: "Trips", value: "19", unit: "" },
//     { title: "Mileage", value: "1", unit: "" },
//     { title: "Time Drive", value: "7.36", unit: "h" },
//     { title: "Average speed", value: "12.78", unit: "mh" },
//     { title: "Max Speed", value: "66.74", unit: "mh" },
//     { title: "Phone Usage", value: "0.00", unit: "%" },
//     { title: "Speeding", value: "0.74", unit: "%" },
//     { title: "Phone Usage Speed", value: "0.37", unit: "%" },
//     { title: "Unique Tags Count", value: "1", unit: "" },
//   ];

//   return (
//     <div className="flex flex-col gap-[5px] min-h-screen 2xl:min-w-[1530px] 2xl:mx-10 pt-[43px]">
//       {/* Header */}
//       <div className="flex justify-between items-center p-1">
//         <div className="text-3xl font-medium">User Profile</div>

//         <div className="flex 2xl:min-w-[350px] gap-4">
//           <button className="border rounded-md p-2 flex items-center gap-2">
//             Delete User <DeleteIcon />
//           </button>

//           <button className="flex items-center border h-[50px] px-8 rounded-md hover:bg-green-700">
//             Export PDF <FiDownload className="ml-2" />
//           </button>

//           <select
//             className="border px-10 py-2 rounded-md"
//             value={statusFilter}
//             onChange={(e) => setStatusFilter(e.target.value)}
//           >
//             <option value="all">Last Week</option>
//             <option value="Last Week">Last 2 Weeks</option>
//             <option value="Last Month">Last Month</option>
//             <option value="Last 2 Month">Last 2 Months</option>
//           </select>
//         </div>
//       </div>

//       {/* User Info */}
//       <div className="grid grid-cols-1 p-2">
//         <div className="grid grid-cols-1 px-4 2xl:min-h-[200px]">
//           <div className="flex items-center justify-between rounded-lg p-2 w-full">
//             <div className="flex flex-col items-start gap-5 h-full pl-4 rounded-lg w-3/5">
//               <div className="2xl:min-w-[80px] 2xl:min-h-[80px] rounded-full bg-[#A5A6F6] flex items-center justify-center text-white font-bold text-xl">
//                 <span role="img" aria-label="avatar">
//                   🧑‍💼
//                 </span>
//               </div>

//               <div className="flex flex-col gap-2">
//                 <h2 className="font-bold text-2xl">User 1</h2>
//                 <div className="flex flex-row gap-4">
//                   <p className="font-[16px] text-gray-500">
//                     User ID: <span className="text-gray-700">ABCDEF123</span>
//                   </p>
//                   <p className="font-[16px] text-gray-500">
//                     Registration Date:{" "}
//                     <span className="text-gray-700">10 September 2025</span>
//                   </p>
//                 </div>
//               </div>
//             </div>

//             <div className="h-full pt-4 pr-6 flex flex-col gap-4 font-medium">
//               <div className="w-full text-base font-medium flex items-center gap-2">
//                 <div className="bg-[#484AB8] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
//                   <Star />
//                 </div>
//                 <span className="text-gray-700">
//                   #2 driver on the list this week
//                 </span>
//               </div>

//               <div className="flex items-center text-base font-medium gap-2">
//                 <div className="bg-[#484AB8] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
//                   <Star />
//                 </div>
//                 <span className="text-gray-700">Speed streak day 6</span>
//               </div>

//               <div className="flex items-center gap-2 text-base font-medium">
//                 <div className="bg-[#AF855A] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
//                   <AlertCircle />
//                 </div>
//                 <span className="text-gray-700">Over speeding sometimes</span>
//               </div>
//             </div>
//           </div>
//         </div>

//         {/* Tabs Section */}
//         <div className="flex flex-col flex-grow rounded-lg p-2">
//           {/* Tab Buttons */}
//           <div className="flex w-1/4 mb-4 text-xl">
//             <button
//               className={`flex-1 text-center ${
//                 activeTab === "Safety Parameters"
//                   ? "text-blue-600 border-b-2 border-blue-600"
//                   : ""
//               }`}
//               onClick={() => setActiveTab("Safety Parameters")}
//             >
//               Safety Parameters
//             </button>

//             <button
//               className={`flex-1 text-center ${
//                 activeTab === "Trips"
//                   ? "text-blue-600 border-b-2 border-blue-600"
//                   : ""
//               }`}
//               onClick={() => setActiveTab("Trips")}
//             >
//               Trips
//             </button>
//           </div>

//           {/* Tab Content */}
//           <div className="flex-grow p-4">
//             {activeTab === "Safety Parameters" && (
//               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 3xl:max-w-[1415px] 3xl:min-h-[400px] 3xl:grid-cols-6 gap-8">
//                 {cards.map((card, idx) => (
//                   <div
//                     key={idx}
//                     className="flex flex-col bg-white mb-4 gap-4 max-w-[209px] max-h-[192px] rounded-xl shadow-sm p-8 hover:shadow-md transition-shadow"
//                   >
//                     <h3 className="text-md font-md text-gray-700">
//                       {card.title}
//                     </h3>
//                     <div className="text-3xl font-bold text-gray-900">
//                       {card.value} {card.unit}
//                     </div>
//                     <p className="font-normal text-sm flex gap-3">
//                       Last Month{" "}
//                       <span className="font-medium text-xs text-green-500 border px-2 rounded-xl">
//                         25%
//                       </span>
//                     </p>
//                   </div>
//                 ))}
//               </div>
//             )}

//             {activeTab === "Trips" && (
//               <div>
//                 <TripsTable />
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default UserDetailsWithTabs;


import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { FiDownload } from "react-icons/fi";
import DeleteIcon from "@mui/icons-material/Delete";
import { Star, AlertCircle } from "lucide-react";
import TripsTable from "./User_TripTable";

const baseURL = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:5000";

function UserDetailsWithTabs() {
  const { userId } = useParams();
  const [statusFilter, setStatusFilter] = useState("last_1_month");
  const [activeTab, setActiveTab] = useState("Safety Parameters");
  const [safetySummary, setSafetySummary] = useState(null);
  const [loading, setLoading] = useState(false);

useEffect(() => {
  if (!userId) return;

  const fetchSafetySummary = async () => {
    console.log("statusFilter", statusFilter);
    setLoading(true);
    try {
      const res = await fetch(
        `${baseURL}/user_safety_dashboard_summary?user_id=${userId}&filter=${statusFilter}`
        //  http://127.0.0.1:5000/user_safety_dashboard_summary?user_id=11&filter=last_1_month
      );
      const data = await res.json();
      setSafetySummary(data);
    } catch (error) {
      console.error("Error fetching safety summary:", error);
    } finally {
      setLoading(false);
    }
  };

  fetchSafetySummary();
}, [userId , statusFilter], );

  if (loading) return <div className=" flex items-center justify-center">Loading...</div>;
  if (!safetySummary)
    return <div className="text-center text-gray-700">No Data Found</div>;

  const cards = [
    { title: "Safety Score", value: safetySummary.safety_score.toFixed(2), unit: "" },
    { title: "Trips", value: safetySummary.trips, unit: "" },
    { title: "Mileage (km)", value: safetySummary.mileage_km.toFixed(2), unit: "km" },
    { title: "Time Driven (min)", value: safetySummary.time_driven_minutes.toFixed(2), unit: "min" },
    { title: "Average Speed (km/h)", value: safetySummary.average_speed_kmh.toFixed(2), unit: "km/h" },
    { title: "Max Speed (km/h)", value: safetySummary.max_speed_kmh.toFixed(2), unit: "km/h" },
    { title: "Phone Usage (%)", value: safetySummary.phone_usage_percentage.toFixed(2), unit: "%" },
  ];

  return (
    <div className="flex flex-col gap-[5px] min-h-screen 2xl:min-w-[1530px] 2xl:mx-10 pt-[43px]">
      {/* Header */}
      <div className="flex justify-between items-center p-1">
        <div className="text-3xl font-medium">User Profile</div>

        <div className="flex 2xl:min-w-[350px] gap-4">
          <button className="border rounded-md p-2 flex items-center gap-2">
            Delete User <DeleteIcon />
          </button>

          <button className="flex items-center border h-[50px] px-8 rounded-md hover:bg-green-700">
            Export PDF <FiDownload className="ml-2" />
          </button>

          <select
            className="border px-10 py-2 rounded-md"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="last_1_week">Last Week</option>
            <option value="last_2_weeks">Last 2 Weeks</option>
            <option value="last_1_month">Last Month</option>
            <option value="last_2_months">Last 2 Months</option>
          </select>
        </div>
      </div>

      {/* User Info */}
      <div className="grid grid-cols-1 p-2">
        <div className="grid grid-cols-1 px-4 2xl:min-h-[200px]">
          <div className="flex items-center justify-between rounded-lg p-2 w-full">
            <div className="flex flex-col items-start gap-5 h-full pl-4 rounded-lg w-3/5">
              <div className="2xl:min-w-[80px] 2xl:min-h-[80px] rounded-full bg-[#A5A6F6] flex items-center justify-center text-white font-bold text-xl">
                <span role="img" aria-label="avatar">
                  🧑‍💼
                </span>
              </div>

              <div className="flex flex-col gap-2">
                <h2 className="font-bold text-2xl">User {userId}</h2>
                <div className="flex flex-row gap-4">
                  <p className="font-[16px] text-gray-500">
                    User ID: <span className="text-gray-700">{userId}</span>
                  </p>
                  <p className="font-[16px] text-gray-500">
                    Registration Date:{" "}
                    <span className="text-gray-700">10 September 2025</span>
                  </p>
                </div>
              </div>
            </div>

            <div className="h-full pt-4 pr-6 flex flex-col gap-4 font-medium">
              <div className="w-full text-base font-medium flex items-center gap-2">
                <div className="bg-[#484AB8] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
                  <Star />
                </div>
                <span className="text-gray-700">
                  #2 driver on the list this week
                </span>
              </div>

              <div className="flex items-center text-base font-medium gap-2">
                <div className="bg-[#484AB8] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
                  <Star />
                </div>
                <span className="text-gray-700">Speed streak day 6</span>
              </div>

              <div className="flex items-center gap-2 text-base font-medium">
                <div className="bg-[#AF855A] text-white rounded-full min-w-[42px] min-h-[42px] flex items-center justify-center">
                  <AlertCircle />
                </div>
                <span className="text-gray-700">Over speeding sometimes</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Section */}
        <div className="flex flex-col flex-grow rounded-lg p-2">
          {/* Tab Buttons */}
          <div className="flex w-1/4 mb-4 text-xl">
            <button
              className={`flex-1 text-center ${
                activeTab === "Safety Parameters"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : ""
              }`}
              onClick={() => setActiveTab("Safety Parameters")}
            >
              Safety Parameters
            </button>

            <button
              className={`flex-1 text-center ${
                activeTab === "Trips"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : ""
              }`}
              onClick={() => setActiveTab("Trips")}
            >
              Trips
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-grow p-4">
            {activeTab === "Safety Parameters" && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 3xl:max-w-[1415px] 3xl:min-h-[400px] 3xl:grid-cols-6 gap-8">
                {cards.map((card, idx) => (
                  <div
                    key={idx}
                    className="flex flex-col bg-white  gap-4 max-w-[209px] max-h-[192px] rounded-xl shadow-sm p-8 hover:shadow-md transition-shadow"
                  >
                    <h3 className="text-md font-md text-gray-700">
                      {card.title}
                    </h3>
                    <div className="text-[24px] font-bold text-gray-900">
                      {card.value} {card.unit}
                    </div>
                    <p className="font-normal text-sm flex gap-3">
                       Last Month{" "}
                       <span className="font-medium text-xs text-green-500 border px-2 rounded-xl">
                         25%
                       </span>
                     </p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "Trips" && (
              <div>
                <TripsTable userId={userId}  statusFilter={statusFilter}/>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserDetailsWithTabs;
