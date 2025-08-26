import React from "react";
import { useNavigate } from "react-router-dom";
import { Clipboard } from "lucide-react";

const users = [
  {
    safetyScore: 44,
    mileage: 12.44,
    registrationDate: "2025/07/03",
    userId: "622ccc22-efd9-45f4-a84f-c4b34bbe2a2e",
    application: "Custom App",
    userGroup: "Common",
    activityStatus: true,
    driverTrips: 2,
    otherTrips: 0,
  },
  {
    safetyScore: 83,
    mileage: 20.44,
    registrationDate: "2025/07/03",
    userId: "4d52b7a4-7c48-4201-ae19-d53de7baeb0d",
    application: "Custom App",
    userGroup: "Common",
    activityStatus: true,
    driverTrips: 1,
    otherTrips: 0,
  },
  {
    safetyScore: 68,
    mileage: 12.89,
    registrationDate: "2025/07/03",
    userId: "b9c87aa7-1233-4075-a211-db937c2f2e40",
    application: "Custom App",
    userGroup: "Common",
    activityStatus: true,
    driverTrips: 3,
    otherTrips: 0,
  },
];

const ListUsers = () => {
  const navigate = useNavigate();

  const getScoreColor = (score: number) => {
    if (score < 50) return "bg-red-100 text-red-600";
    if (score < 70) return "bg-yellow-100 text-yellow-600";
    return "bg-orange-100 text-orange-700";
  };

  return (
    <div className="p-6 bg-white min-h-screen">
      <div className="flex justify-between mb-4 items-center">
        <input
          type="text"
          placeholder="Search by User"
          className="border px-4 py-2 w-1/3 rounded-md"
        />
        <div className="flex gap-2">
          <button className="bg-green-500 text-white px-4 py-2 rounded-md">
            Add User(s)
          </button>
          <button className="bg-gray-100 text-sm px-3 py-2 rounded-md border">
            Add Filters
          </button>
          <button className="bg-gray-100 text-sm px-3 py-2 rounded-md border">
            Columns ▼
          </button>
          <button className="flex items-center gap-1 bg-gray-100 px-3 py-2 rounded-md border">
            <img src="https://www.svgrepo.com/show/374118/csv.svg" className="h-4" />
            Export Data
          </button>
        </div>
      </div>

      <table className="w-full text-sm border shadow-sm">
        <thead className="bg-gray-100 text-gray-700">
          <tr>
            <th className="p-2 text-left">Safety Score</th>
            <th className="p-2 text-left">Mileage</th>
            <th className="p-2 text-left">Registration Date</th>
            <th className="p-2 text-left">User ID</th>
            <th className="p-2 text-left">Application</th>
            <th className="p-2 text-left">User Group</th>
            <th className="p-2 text-left">Activity Status</th>
            <th className="p-2 text-left">Driver Trips Count</th>
            <th className="p-2 text-left">Other Trips Count</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr
              key={user.userId}
              className="hover:bg-gray-50 border-t"
            >
              <td className={`p-2 ${getScoreColor(user.safetyScore)} rounded-md`}>
                {user.safetyScore}
              </td>
              <td className="p-2">{user.mileage}</td>
              <td className="p-2">{user.registrationDate}</td>
              <td
                className="p-2 text-blue-600 underline cursor-pointer flex items-center gap-1"
                onClick={() => navigate(`/profile/${user.userId}`)}
              >
                {user.userId}
                <Clipboard className="h-3 w-3" />
              </td>
              <td className="p-2">{user.application}</td>
              <td className="p-2">{user.userGroup}</td>
              <td className="p-2">{user.activityStatus ? "🟢" : "🔴"}</td>
              <td className="p-2">{user.driverTrips}</td>
              <td className="p-2">{user.otherTrips}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-4 text-sm text-gray-600">1 - 3 of 3</div>
    </div>
  );
};

export default ListUsers;
