import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  ChevronDown,
  ChevronRight,
  LayoutDashboard,
  Users,
  Map,
  Folder,
  FileText,
  FileCog,
  BookOpen,
  Bug,
} from "lucide-react";

const SidebarSection: React.FC<{
  title: string;
  icon: React.ReactNode;
  children?: React.ReactNode;
}> = ({ title, icon, children }) => {
  const [open, setOpen] = useState(true);

  return (
    <div className="space-y-1">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-2 text-left text-white hover:bg-gray-800"
      >
        <span className="flex items-center gap-3">
          {icon}
          <span className="text-base font-semibold">{title}</span>
        </span>
        {children &&
          (open ? <ChevronDown size={16} /> : <ChevronRight size={16} />)}
      </button>
      {open && children && <div className="ml-10 mt-1">{children}</div>}
    </div>
  );
};

const SidebarLink: React.FC<{ to: string; label: string }> = ({
  to,
  label,
}) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `block px-2 py-1 text-sm rounded-md mb-1 ${
        isActive
          ? "bg-gray-700 text-white"
          : "text-gray-400 hover:bg-gray-800 hover:text-white"
      }`
    }
  >
    {label}
  </NavLink>
);

const StaticSection: React.FC<{ icon: React.ReactNode; label: string }> = ({
  icon,
  label,
}) => (
  <div className="flex items-center gap-3 px-4 py-2 text-white text-base font-semibold hover:bg-gray-800 rounded-md">
    {icon}
    <span>{label}</span>
  </div>
);

const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-900 text-white h-screen sticky top-0 flex flex-col">
      <div className="text-2xl font-bold px-6 py-4 border-b border-gray-800">
        DataHub
      </div>

      <nav className="flex-1 px-2 py-4 overflow-y-auto space-y-12">
        <SidebarSection title="Dashboards" icon={<LayoutDashboard size={24} />}>
          <SidebarLink to="/dashboard/summary" label="Summary" />
          {/* <SidebarLink to="/dashboard/sdk" label="SDK" /> */}
          <SidebarLink to="/dashboard/safety" label="Safety" />
        </SidebarSection>

        <SidebarSection title="Users" icon={<Users size={24} />}>
          <SidebarLink to="/users/list" label="List of Users" />
          <SidebarLink to="/users/profiles" label="Profiles" />
          <SidebarLink to="/users/permissions" label="Permissions" />
        </SidebarSection>

        <SidebarSection title="Trips" icon={<Map size={24} />}>
          <SidebarLink to="/trips/list" label="List of Trips" />
          <SidebarLink to="/trips/details" label="Trip Details" />
        </SidebarSection>

        <div className="space-y-2 pt-2 border-t border-gray-800">
          <SidebarLink to="/management" label="Management" />
          <StaticSection icon={<FileText size={22} />} label="Billing" />
          <SidebarLink to="/data-tool" label="DataTool" />
          <StaticSection icon={<BookOpen size={22} />} label="User Guide" />
          <StaticSection icon={<Bug size={22} />} label="Report a Bug" />
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;
