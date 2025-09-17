import { Outlet, useLocation } from "react-router-dom";
import Header from "../components/Header";
import Sidebar from "../components/New_Sidebar";

const DashboardLayout = () => {
  const location = useLocation();

  const hideHeaderRoutes = ["/trips"];

  const shouldHideHeader =
    hideHeaderRoutes.some((path) => location.pathname.startsWith(path));

  return (
    <div className="flex h-screen w-screen xl:bg-gray-100 overflow-hidden">
      <div>
        <Sidebar />
      </div>

      <div className="flex flex-col 2xl:w-full xl:w-full xl:bg-gray-200 2xl:bg-[#f7f7f7]">
        {/* Render Header only when not on Trips or Trip Details */}
        {!shouldHideHeader && <Header />}
        
        <main className="overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
