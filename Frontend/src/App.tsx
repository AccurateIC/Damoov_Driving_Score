import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";

import Summary from "./pages/Dashboard/Summary";
// import SDK from "./pages/Dashboard/SDK";
import Safety from "./pages/Dashboard/Safety";

import UsersList from "./pages/Users/List";
import Profiles from "./pages/Users/Profiles";
import Permissions from "./pages/Users/Permissions";

import TripsList from "./pages/trips/TripsList";
import TripDetails from "./pages/trips/TripDetails";

import Management from "./pages/Management";
import Billing from "./pages/Billing";
import DataTool from "./pages/DataTool";
import UserGuide from "./pages/UserGuide";
import ReportBug from "./pages/ReportBug";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          {/* Redirect /dashboard → /dashboard/summary */}
          <Route
            path="dashboard"
            element={<Navigate to="/dashboard/summary" replace />}
          />

          <Route path="dashboard/summary" element={<Summary />} />
          {/* <Route path="dashboard/sdk" element={<SDK />} /> */}
          <Route path="dashboard/safety" element={<Safety />} />

          <Route path="users/list" element={<UsersList />} />
          <Route path="users/profiles" element={<Profiles />} />
          <Route path="users/permissions" element={<Permissions />} />

          <Route path="trips/list" element={<TripsList />} />
          <Route path="/trips/details" element={<TripDetails />} />

          <Route path="Management" element={<Management />} />
          <Route path="billing" element={<Billing />} />
          <Route path="data-tool" element={<DataTool />} />
          <Route path="user-guide" element={<UserGuide />} />
          <Route path="report-bug" element={<ReportBug />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
