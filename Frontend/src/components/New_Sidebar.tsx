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
import logo from "../assets/accurate_logo.png"; // Adjust the path as necessary

const Sidebar = () => {
  const [openDashboard, setOpenDashboard] = useState(true);

  return (
    <aside className="w-64 bg-neutral-100 text-white h-screen sticky top-0 flex flex-col items-center py-6">
      {/* Logo */}
      <div className="flex flex-col items-center mb-12">
        <img
          src="../assets/accurate_logo.png" // replace with your actual logo path
          alt="Accurate Group"
          className="h-12 object-contain"
        />
        <p className="text-xs text-gray-400 mt-2 tracking-wide text-center">
          INNOVATION FOR PROGRESS
        </p>
      </div>

      {/* Dashboard Section */}
      <div className="w-11/12">
        <button
          onClick={() => setOpenDashboard(!openDashboard)}
          className="w-full flex items-center justify-between bg-neutral-900 rounded-full px-4 py-2 hover:bg-neutral-800"
        >
          <span className="flex items-center gap-2">
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </span>
          {openDashboard ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>

        {/* Dashboard Sub-links */}
        {openDashboard && (
          <div className="mt-4 flex flex-col gap-4 ml-6">
            <NavLink
              to="/dashboard/summary_New"
              className={({ isActive }) =>
                `flex items-center gap-2 ${
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
                `flex items-center gap-2 ${
                  isActive
                    ? "text-indigo-500"
                    : "text-gray-400 hover:text-white"
                }`
              }
            >
              <Shield size={18} />
              <span>Safety</span>
            </NavLink>
          </div>
        )}
      </div>

      {/* Other Sections */}
      <nav className="flex flex-col gap-6 w-full px-8 mt-8">
        <NavLink
          to="/users/list"
          className={({ isActive }) =>
            `flex items-center gap-2 ${
              isActive ? "text-indigo-500" : "text-gray-400 hover:text-white"
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
            `flex items-center gap-2 ${
              isActive ? "text-indigo-500" : "text-gray-400 hover:text-white"
            }`
          }
        >
          <Route size={18} />
          <span>Trips</span>
        </NavLink>

        <NavLink
          to="/user-guide"
          className={({ isActive }) =>
            `flex items-center gap-2 ${
              isActive ? "text-indigo-500" : "text-gray-400 hover:text-white"
            }`
          }
        >
          <BookOpen size={18} />
          <span>User Guide</span>
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
