import { Navigate } from "react-router-dom";
import Summary from "./pages/Dashboard/Summary_New";
import SDK from "./pages/Dashboard/SDK";
import Safety from "./pages/Dashboard/New_Safety";
import UsersList from "./pages/Users/New_Users";
import User_Details from "./pages/Users/User_Details";
import Profiles from "./pages/Users/Profiles";
import Trips from "./pages/trips/New_Trips";
import New_Trips_Detailed from "./pages/trips/New_Trips_Detailed";
import TripDetails from "./pages/trips/TripDetails";
import Management from "./pages/Management";
import Billing from "./pages/Billing";
import DataTool from "./pages/DataTool";
import UserGuide from "./pages/UserGuide";
import ReportBug from "./pages/ReportBug";
import TripMap from "./pages/trips/TripMap";

export const routes = [
  {
    path: "",
    element: <Navigate to="summary_New" replace />, // default dashboard redirect
  },
  {
    path: "summary_New",
    element: <Summary />,
  },
  {
    path: "sdk",
    element: <SDK />,
    hideHeader: true,
  },
  {
    path: "safety",
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
    element: <Trips />,
  },
  {
    path: "trips/details/:unique_id",
    element: <New_Trips_Detailed />,
    hideHeader: true,
  },

{
  path: "trips/details/:track_id",
  element: <TripDetails />,
  hideHeader: true,
},
  {
    path: "trips/details",
    element: <TripDetails />,
  },
  {
    path: "management",
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

// // src/routes.ts
// import { Navigate } from "react-router-dom";
// import Summary from "./pages/Dashboard/Summary_New";
// import SDK from "./pages/Dashboard/SDK";
// import Safety from "./pages/Dashboard/New_Safety";
// import UsersList from "./pages/Users/New_Users";
// import User_Details from "./pages/Users/User_Details";
// import Profiles from "./pages/Users/Profiles";
// import TripsList from "./pages/trips/TripsList";
// import Trips from "./pages/trips/New_Trips";
// import TripDetails from "./pages/trips/TripDetails";
// import New_Trips_Detailed from "./pages/trips/New_Trips_Detailed";
// import New_Trips from "./pages/trips/New_Trips";
// import Management from "./pages/Management";
// import Billing from "./pages/Billing";
// import DataTool from "./pages/DataTool";
// import UserGuide from "./pages/UserGuide";
// import ReportBug from "./pages/ReportBug";
// import { elements } from "chart.js";

// export const routes = [
//   {
//     path: "dashboard",
//     element: <Navigate to="/dashboard/summary_New" replace />,
//   },
//   {
//     path: "dashboard/summary_New",
//     element: <Summary />,
//   },
//   {
//     path: "dashboard/sdk",
//     element: <SDK />,
//     hideHeader: true, // hide header
//   },
//   {
//     path: "dashboard/safety",
//     element: <Safety />,
//   },
//   {
//     path: "users/list",
//     element: <UsersList />,
//   },
//   {
//     path: "users/profiles",
//     element: <Profiles />,
//   },
//   {
//     path: "users/:userId",
//     element: <User_Details />,
//     hideHeader: true,
//   },
//     {
//     path: "trips/list",
//     element: <Trips />,
//   },
//   // {
//   //   path: "trips/list",
//   //   element: <TripsList />,
//   // },
//   {
//     path: "trips/:tripId",
//     element: <New_Trips_Detailed />,
//     hideHeader: true,
//   },
//   {
//     path: "trips/details",
//     element: <TripDetails />,
//   },
//   {
//     path: "Management",
//     element: <Management />,
//   },
//   {
//     path: "billing",
//     element: <Billing />,
//   },
//   {
//     path: "data-tool",
//     element: <DataTool />,
//   },
//   {
//     path: "user-guide",
//     element: <UserGuide />,
//   },
//   {
//     path: "report-bug",
//     element: <ReportBug />,
//   },
// ];
