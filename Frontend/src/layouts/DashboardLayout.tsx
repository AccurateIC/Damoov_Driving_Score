// src/layouts/DashboardLayout.tsx
import { Outlet } from "react-router-dom";
import Header from "../components/Header";
// import Sidebar from '../components/Sidebar';
import Sidebar from "../components/New_Sidebar";

const DashboardLayout = () => {
  return (
    <div className="flex h-screen gap-[32px] bg-gray-50  overflow-hidden">
     <div> <Sidebar /></div>

      <div className="flex flex-col  flex-1">
        <Header />
        <main className="flex-1 overflow-y-auto  p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
