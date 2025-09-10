// import React from "react";
// import { FiSearch, FiDownload } from "react-icons/fi";
// import DeleteIcon from "@mui/icons-material/Delete";
// function User_Details() {
//   const [statusFilter, setStatusFilter] = React.useState("all"); // NEW
//   return (
//     <div className="flex flex-col gap-[5px] bg-amber-100 min-h-screen 2xl:min-w-[1081px] 2xl:mx-10">
//       <div className="flex justify-between bg-amber-300 items-center ">
//         <div className=" text-3xl font-medium ">User Profile </div>
//         <div className="flex  2xl:min-w-[350px] gap-4 ">
//           <button className="border rounded-md p-2">
//             Delete User
//             <DeleteIcon />
//           </button>
//           <button className="flex items-center border h-[50px] px-8  rounded-md hover:bg-green-700">
//             Export PDF <FiDownload className="ml-2 " />
//           </button>
//           <select
//             className="border px-10 py-2 rounded-md "
//             value={statusFilter}
//             onChange={(e) => setStatusFilter(e.target.value)}
//           >
//             <option value="all">All</option>
//             <option value="active">Active</option>
//             <option value="inactive">Inactive</option>
//           </select>
//         </div>
//       </div>

//       <div className=" bg-amber-600  min-h-screen grid grid-cols-1 gap-10 p-4">
//         <div className="grid grid-cols-2 h-[178px] bg-amber-400 gap-10 p-4">
//           <div className=" bg-amber-500">hello</div>
//           <div className=" bg-amber-500">heelo2</div>
//         </div>
//         <div className="min-h-screen bg-amber-700">h3</div>
//       </div>
//     </div>
//   );
// }

// export default User_Details;

import React from "react";
import { FiDownload } from "react-icons/fi";
import DeleteIcon from "@mui/icons-material/Delete";
import { Star, AlertCircle } from "lucide-react";
import Tabs from "./dummtTab";

function User_Details() {
  const [statusFilter, setStatusFilter] = React.useState("all"); // NEW

  return (
    <div className="flex flex-col gap-[5px] min-h-screen 2xl:min-w-[1530px] 2xl:mx-10 pt-[43px]">
      {/* Header */}
      <div className="flex justify-between  items-center p-1">
        <div className=" text-3xl font-medium ">User Profile</div>
        <div className="flex 2xl:min-w-[350px] gap-4">
          <button className="border rounded-md p-2 flex items-center gap-2">
            Delete User
            <DeleteIcon />
          </button>
          <button className="flex items-center border h-[50px] px-8 rounded-md hover:bg-green-700">
            Export PDF <FiDownload className="ml-2 " />
          </button>
          <select
            className="border px-10 py-2 rounded-md"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">Last Week</option>
            <option value="Last Week">Last 2 Week</option>
            <option value="Last  Month">Last Month</option>
           < option value="Last 2 Month">Last 2 Month</option>
          </select>
        </div>
      </div>

      <div className=" grid grid-cols-1 p-2 bg-">
        <div className="grid grid-cols-1 px-4 2xl:min-h-[200px] ">
          <div className="flex items-center  justify-between  rounded-lg  p-2 w-full">
            <div className="flex flex-col  items-start  gap-5 h-full pl-4 rounded-lg w-3/5">
              <div className="2xl:min-w-[80px] 2xl:min-h-[80px] rounded-full bg-[#A5A6F6] bg- flex items-center justify-center text-white font-bold text-xl">
                <span role="img" aria-label="avatar">
                  🧑‍💼
                </span>
              </div>
              <div className="flex flex-col gap-2">
                <h2 className="font-bold text-2xl">User 1</h2>
                <div className="flex flex-row gap-4">
                  {" "}
                  <p className="font-[16px] text-gray-500">
                    User ID: <span className="text-gray-700">ABCDEF123</span>
                  </p>
                  <p className="font-[16px] text-gray-500">
                    Registration Date:{" "}
                    <span className="text-gray-700">10 Sepember 2025</span>
                  </p>
                </div>
              </div>
            </div>
            {/* Right Section */}
            <div className="h-full pt- pr-6 flex flex-col gap-4 font-medium ">
              <div className="w-full text-base font-medium flex items-center gap-2  ">
                <div className="bg-[#484AB8] text-white rounded-full 3xl:min-w-[42px] 3xl:min-h-[42px] flex items-center justify-center  ">
                  <Star />
                </div>
                <span className=" text-gray-700">
                  #2 driver on the list this week
                </span>
              </div>

              <div className="flex items-center text-base font-medium gap-2 ">
                <div className="bg-[#484AB8] text-white rounded-full 3xl:min-w-[42px] 3xl:min-h-[42px] flex items-center justify-center ">
                  <Star  />
                </div>
                <span className=" text-gray-700">Speed streak day 6</span>
              </div>

              <div className="flex items-center gap-2 text-base font-medium">
                <div className="bg-[#AF855A] 3xl:min-w-[42px] 3xl:min-h-[42px] text-white rounded-full flex items-center justify-center ">
                  <AlertCircle  />
                </div>
                <span className=" text-gray-700">Over speeding sometimes</span>
              </div>
            </div>
          </div>
        </div>

        {/* Other content */}
        <div className="flex flex-col flex-grow  rounded-lg p-2">
          <Tabs />
        </div>
      </div>
    </div>
  );
}

export default User_Details;
