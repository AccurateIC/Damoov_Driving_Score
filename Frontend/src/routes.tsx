// src/routes.ts
import { Navigate } from "react-router-dom";
import Summary from "./pages/Dashboard/Summary_New";
import SDK from "./pages/Dashboard/SDK";
import Safety from "./pages/Dashboard/New_Safety";
import UsersList from "./pages/Users/New_Users";
import User_Details from "./pages/Users/User_Details";
import Profiles from "./pages/Users/Profiles";
import TripsList from "./pages/trips/TripsList";
import TripDetails from "./pages/trips/TripDetails";
import Management from "./pages/Management";
import Billing from "./pages/Billing";
import DataTool from "./pages/DataTool";
import UserGuide from "./pages/UserGuide";
import ReportBug from "./pages/ReportBug";

export const routes = [
  {
    path: "dashboard",
    element: <Navigate to="/dashboard/summary_New" replace />,
  },
  {
    path: "dashboard/summary_New",
    element: <Summary />,
   
  },
  {
    path: "dashboard/sdk",
    element: <SDK />,
    hideHeader: true, // hide header
  },
  {
    path: "dashboard/safety",
    element: <Safety />,
    
  },
  {
    path: "users/list",
    element: <UsersList />,
  },
  {
    path: "users/profiles",
    element: <Profiles />,
  },
  {
    path: "users/:userId",
    element: <User_Details />,
    hideHeader: true,
  },
  {
    path: "trips/list",
    element: <TripsList />,
  },
  {
    path: "trips/details",
    element: <TripDetails />,
  },
  {
    path: "Management",
    element: <Management />,
  },
  {
    path: "billing",
    element: <Billing />,
  },
  {
    path: "data-tool",
    element: <DataTool />,
  },
  {
    path: "user-guide",
    element: <UserGuide />,
  },
  {
    path: "report-bug",
    element: <ReportBug />,
  },
];
