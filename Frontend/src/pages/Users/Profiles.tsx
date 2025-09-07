import React, { useState, useRef } from "react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { FiCopy } from "react-icons/fi";

const profilesData: Record<string, any> = {
  "622ccc22-efd9-45f4-a84f-c4b34bbe2a2e": {
    name: "Unknown",
    status: "Active",
    email: "Unknown",
    phone: "Unknown",
    clientId: "No data",
    company: "Accurate Industrial Controls Pvt Ltd",
    group: "Common",
    app: "Custom App",
    timeDriven: "23 m",
    mileage: 12,
    trips: 2,
    registrationDate: "2025/07/03",
    latestTrack: "2025/07/03",
    latestStatus: "No data",
    lifetime: "0d",
    os: "No Data",
    phoneModel: "No data",
    appVersion: "No data",
    sdkVersion: "No data",
    nickname: "Unknown",
    gender: "Unknown",
    birthday: "Unknown",
    children: "Unknown",
    married: "Unknown",
    latestScoringDate: "2025/07/11",
    safetyScore: 44,
    ecoScore: 88,
    trustLevel: 100,
    scorePeriod: "Up to date", 
    driverScore: 0,
    penaltyScore: -17,
    userId: "622ccc22-efd9-45f4-a84f-c4b34bbe2a2e",
  },
  "b9c87aa7-1233-4075-a211-db937c2f2e40": {
    name: "Driver C",
    status: "Active",
    email: "driverc@xyz.com",
    phone: "9876543210",
    clientId: "XYZ1234",
    company: "XYZ Logistics",
    group: "Common",
    app: "Custom App",
    timeDriven: "60 m",
    mileage: 12.89,
    trips: 3,
    registrationDate: "2025/07/03",
    latestTrack: "2025/07/03",
    latestStatus: "2025/07/10",
    lifetime: "3d",
    os: "Android",
    phoneModel: "OnePlus",
    appVersion: "v1.2.3",
    sdkVersion: "v4.5.6",
    nickname: "C Driver",
    gender: "Male",
    birthday: "1995-05-05",
    children: "2",
    married: "Yes",
    latestScoringDate: "2025/07/11",
    safetyScore: 68,
    ecoScore: 82,
    trustLevel: 90,
    scorePeriod: "Up to date",
    driverScore: 5,
    penaltyScore: -12,
    userId: "b9c87aa7-1233-4075-a211-db937c2f2e40",
  }
};

const Profiles = () => {
  const [inputId, setInputId] = useState("");
  const [user, setUser] = useState<any>(null);
  const [notFound, setNotFound] = useState(false);
  const [activeTab, setActiveTab] = useState("Trips");
  const cardRef = useRef(null);

  const handleSearch = () => {
    const userData = profilesData[inputId.trim()];
    if (userData) {
      setUser(userData);
      setNotFound(false);
    } else {
      setUser(null);
      setNotFound(true);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(user.userId);
    alert("User ID copied!");
  };

  const handleExport = async () => {
    if (!cardRef.current) return;
    const canvas = await html2canvas(cardRef.current);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF();
    pdf.addImage(imgData, "PNG", 10, 10, 190, 0);
    pdf.save("profile.pdf");
  };

  return (
    <div className="p-6 bg-[#f8f9fb] min-h-screen text-sm">
      <div className="flex items-center gap-3 mb-4">
        <button className="px-4 py-2 border rounded-md bg-white">← Back</button>
        <input
          value={inputId}
          onChange={(e) => setInputId(e.target.value)}
          className="flex-1 px-4 py-2 border rounded-md"
          placeholder="Enter User ID"
        />
        <button onClick={handleSearch} className="bg-blue-600 text-white px-4 py-2 rounded-md">
          Search
        </button>
        <button onClick={handleExport} className="bg-purple-600 text-white px-4 py-2 rounded-md">
          Export PDF
        </button>
        <div className="ml-auto">
          <span className="font-medium">Permissions Status:</span>
          <span className="ml-2 bg-gray-100 text-gray-800 px-2 py-1 rounded-md text-xs">NO DATA</span>
        </div>
      </div>

      {notFound && <div className="text-red-600 mb-4">User Not Found</div>}

      {user && (
        <>
          <div ref={cardRef} className="bg-white rounded-xl shadow p-6 grid grid-cols-12 gap-6">
            <div className="col-span-3 space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-gray-200" />
                <div>
                  <h2 className="font-semibold text-base">{user.name}</h2>
                  <p className="text-green-600 text-xs">● {user.status}</p>
                </div>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md">New Driver Profile</button>
              <div className="space-y-2">
                <div className="border border-green-500 text-green-700 bg-green-50 px-3 py-1 rounded-md">
                  Score Period: {user.scorePeriod}
                </div>
                <div className="bg-red-100 text-red-600 px-3 py-1 rounded-md">Safety Score: {user.safetyScore}</div>
                <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-md">Eco Score: {user.ecoScore}</div>
                <div className="bg-green-100 text-green-700 px-3 py-1 rounded-md">Trust Level: {user.trustLevel}</div>
                <div className="flex gap-2">
                  <div className="bg-blue-100 px-3 py-1 rounded-md text-blue-800">{user.driverScore}</div>
                  <div className="bg-green-100 px-3 py-1 rounded-md text-green-800">{user.penaltyScore}</div>
                </div>
              </div>
            </div>

            <div className="col-span-9 grid grid-cols-3 gap-4 text-gray-800">
              <div><strong>Email:</strong> {user.email}</div>
              <div><strong>Phone:</strong> {user.phone}</div>
              <div><strong>Client ID:</strong> {user.clientId}</div>

              <div>
                <strong>User ID:</strong> {user.userId}
                <FiCopy onClick={handleCopy} className="inline ml-1 cursor-pointer text-gray-500" />
              </div>
              <div><strong>Company:</strong> {user.company}</div>
              <div><strong>Application:</strong> {user.app}</div>

              <div><strong>Group:</strong> {user.group}</div>
              <div><strong>Time Driven:</strong> {user.timeDriven}</div>
              <div><strong>Mileage:</strong> {user.mileage} (mi)</div>

              <div><strong>Trips / Driver Trips:</strong> {user.trips} / {user.trips}</div>
              <div><strong>Registration Date:</strong> {user.registrationDate}</div>
              <div><strong>Latest Track Date:</strong> {user.latestTrack}</div>

              <div><strong>Latest Status Date:</strong> {user.latestStatus}</div>
              <div><strong>Lifetime:</strong> {user.lifetime}</div>
              <div><strong>OS:</strong> {user.os}</div>

              <div><strong>Phone Model:</strong> {user.phoneModel}</div>
              <div><strong>App Version:</strong> {user.appVersion}</div>
              <div><strong>SDK Version:</strong> {user.sdkVersion}</div>

              <div><strong>Nickname:</strong> {user.nickname}</div>
              <div><strong>Gender:</strong> {user.gender}</div>
              <div><strong>Birthday:</strong> {user.birthday}</div>

              <div><strong>Children:</strong> {user.children}</div>
              <div><strong>Married:</strong> {user.married}</div>
              <div><strong>Latest Scoring Date:</strong> {user.latestScoringDate}</div>
            </div>
          </div>

          <div className="mt-6 flex gap-6 text-sm font-medium text-gray-700">
            {["Trips", "Safety Dashboard", "Vehicles & Devices"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-md ${
                  activeTab === tab ? "bg-blue-100 text-blue-800" : "hover:text-blue-600"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="mt-4 bg-white rounded shadow p-4">
            <p className="text-gray-600">You are viewing the <strong>{activeTab}</strong> section.</p>
          </div>
        </>
      )}
    </div>
  );
};

export default Profiles;
