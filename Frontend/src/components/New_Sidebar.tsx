import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  ChevronDown,
  ChevronUp,
  LayoutDashboard,
  FileText,
  Shield,

  Users,
  Route,
  BookOpen,
} from "lucide-react";
import { AiOutlineSafety } from "react-icons/ai";
import logo from "../assets/logo.png"; // Adjust the path as necessary

const Sidebar = () => {
  const [openDashboard, setOpenDashboard] = useState(true);

  return (
    <aside className=" md:w-[295px]   md:h-[1024px]  text-white h-screen sticky top-0 flex flex-col items-center py-6">
      {/* Logo */}
      <div className="md:w-[231px]  md:h-[944px] mx-[32px] my-[42px]">
        <div className="flex flex-col items-center w-[231px] h-[50px] mb-12">
          <img
            src={logo} // replace with your actual logo path
            alt="Accurate Group"
            className="h-12 object-contain"
          />
        </div>

        {/* Dashboard Section */}
        <div className=" -400 md:h-[502px] md:w-[231px] gap-6 ">
          <div className="items-center  md:w-[231px]  gap-5  ">
            <button
              onClick={() => setOpenDashboard(!openDashboard)}
              className="w-[231px] h-[71px] flex items-center justify-between bg-neutral-900 rounded-full px-4 py-2 hover:bg-neutral-800"
            >
              <span className="flex items-center ">
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </span>
              {openDashboard ? (
                <ChevronUp size={16} />
              ) : (
                <ChevronDown size={16} />
              )}
            </button>

            {/* Dashboard Sub-links */}
            {openDashboard && (
              <div className="mt-4 flex flex-col   gap-4 ml-6">
                <NavLink
                  to="/dashboard/summary_New"
                  className={({ isActive }) =>
                    `flex items-center gap-2   h-[57px] font-semibold text-xl pt-4 pr-12 pb-4 pl-12px ${
                      isActive
                        ? "text-indigo-500"
                        : "text-gray-400 hover:text-white"
                    }`
                  }
                >
                  <FileText size={18} />
                  <span>Summary</span>
                </NavLink>

                <NavLink
                  to="/dashboard/safety"
                  className={({ isActive }) =>
                    `flex items-center   h-[57px] gap-2 font-semibold text-xl pt-4 pr-12 pb-4 pl-12px  ${
                      isActive
                        ? "text-indigo-500"
                        : "text-gray-400 hover:text-white"
                    }`
                  }
                >
                  <AiOutlineSafety size={20} />
                  <span>Safety</span>
                </NavLink>
              </div>
            )}
          </div>

          {/* Other Sections */}
          <nav className="flex flex-col gap-6 w-full px-8 mt-8 ">
            <NavLink
              to="/users/list"
              className={({ isActive }) =>
                `flex items-center gap-2 font-semibold text-xl  ${
                  isActive
                    ? "text-indigo-500"
                    : "text-gray-400 hover:text-white"
                }`
              }
            >
              <Users size={18} />
              <span>Users</span>
            </NavLink>

            <NavLink
              // to="/trips/list"
              to="/trips/details"
              className={({ isActive }) =>
                `flex items-center gap-2 font-semibold text-xl py-6 ${
                  isActive
                    ? "text-indigo-500"
                    : "text-gray-400 hover:text-white"
                }`
              }
            >
              <Route size={18} />
              <span>Trips</span>
            </NavLink>

            <NavLink
              to="/user-guide"
              className={({ isActive }) =>
                `flex items-center gap-2 font-semibold text-xl ${
                  isActive
                    ? "text-indigo-500"
                    : "text-gray-400 hover:text-white"
                }`
              }
            >
              <BookOpen size={18} />
              <span>User Guide</span>
            </NavLink>
          </nav>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
