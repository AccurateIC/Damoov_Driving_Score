import { Outlet, useLocation } from "react-router-dom";
import Header from "../components/Header";
import Sidebar from "../components/New_Sidebar";
import { routes } from "../routes";

const DashboardLayout = () => {
  const location = useLocation();

  const currentRoute = routes.find(route => {
      if (!route.path) return false; // guard clause
    if (route.path.includes(":")) {
      const basePath = route.path.split("/:")[0];
      return location.pathname.startsWith("/" + basePath);
    }
    return location.pathname === "/" + route.path;
  });

  const hideHeader = currentRoute?.hideHeader || false;

  return (
    <div className="flex h-screen w-screen xl:bg-gray-100 2xl:bg-amber-10 overflow-hidden">
      <Sidebar />
      <div className="flex flex-col xl:bg-gray-200 2xl:bg-[#f7f7f7] 2xl:w-full xl:w-full">
        {!hideHeader && <Header />}
        <main className="overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;


// // src/layouts/DashboardLayout.tsx
// import { Outlet } from "react-router-dom";
// import Header from "../components/Header";
// // import Sidebar from '../components/Sidebar';
// import Sidebar from "../components/New_Sidebar";

// const DashboardLayout = () => {
//   return (
//     <div className="flex h-screen w-screen xl:bg-gray-100  2xl:bg-amber-10 overflow-hidden">
//       <div>
//         {" "}
//         <Sidebar />
//       </div>

//       <div className="flex flex-col xl:bg-gray-200 2xl:bg-[#f7f7f7] 2xl:w-full xl:w-full">
//         <Header />
//         <main className=" overflow-y-auto  ">
//           <Outlet />
//         </main>
//       </div>
//     </div>
//   );
// };

// export default DashboardLayout;
