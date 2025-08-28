// src/layouts/DashboardLayout.tsx
import { Outlet } from "react-router-dom";
import Header from "../components/Header";
// import Sidebar from '../components/Sidebar';
import Sidebar from "../components/New_Sidebar";

const DashboardLayout = () => {
  return (
    <div className="flex h-screen w-screen xl:bg-gray-100  2xl:bg-amber-10 overflow-hidden">
     <div> <Sidebar /></div>

      <div className="flex xl:bg-gray-200 
       2xl:bg-[#f7f7f7] 
    // 2xl:bg-gray-150 
    flex-col 2xl:w-full xl-w-full">
        <Header />
        <main className=" overflow-y-auto  ">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
