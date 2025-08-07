// Management.tsx
import React from "react";

const Management = () => {
  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="text-xl font-semibold text-gray-800">Management</div>

      {/* Main Sections */}
      <div className="grid grid-cols-4 gap-6">
        {/* Company Column */}
        <div className="bg-white rounded shadow p-4 space-y-4">
          <h3 className="font-semibold text-gray-700">Company</h3>
          <select className="border p-2 rounded text-sm w-full">
            <option>Accurate Industrial Controls Pvt Ltd</option>
          </select>
          <ul className="space-y-2 text-sm text-gray-600">
            <li>🏢 Company Settings</li>
            <li>🔐 Admin Credentials</li>
            <li>🔑 Access Management</li>
            <li>💳 Billing</li>
          </ul>
        </div>

        {/* Application Column */}
        <div className="bg-white rounded shadow p-4 space-y-4">
          <h3 className="font-semibold text-gray-700 flex justify-between">
            Application <span className="text-green-600 text-xs cursor-pointer">Create Application</span>
          </h3>
          <select className="border p-2 rounded text-sm w-full">
            <option>Custom App</option>
          </select>
          <ul className="space-y-2 text-sm text-gray-600">
            <li>⚙️ Application Settings</li>
            <li>📦 SDK Installation</li>
            <li>🛠️ DataTool</li>
            <li>📤 Data Export</li>
            <li>🔐 Access Management</li>
          </ul>
        </div>

        {/* User Group Column */}
        <div className="bg-white rounded shadow p-4 space-y-4">
          <h3 className="font-semibold text-gray-700 flex justify-between">
            User Group <span className="text-green-600 text-xs cursor-pointer">Create User Group</span>
          </h3>
          <select className="border p-2 rounded text-sm w-full">
            <option>Common</option>
          </select>
          <ul className="space-y-2 text-sm text-gray-600">
            <li>⚙️ Group Settings</li>
            <li>📡 Real-time data</li>
            <li>📅 Schedule</li>
            <li>🧾 User Group Credentials</li>
            <li>🔁 Backend Callbacks</li>
            <li>📤 Data Export</li>
            <li>🎟️ Invitation Code</li>
            <li>💰 DriveCoins</li>
            <li>🔐 Access Management</li>
          </ul>
        </div>

        {/* How to Start Column */}
        <div className="bg-white rounded shadow p-4 space-y-4">
          <h3 className="font-semibold text-gray-700 text-center">How to Start</h3>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="border p-3 rounded">
              <strong>📦 Integrate tracking SDK</strong>
              <p className="text-xs mt-1">Install telematics SDK to your application to start tracking telematics data.</p>
            </div>
            <div className="border p-3 rounded">
              <strong>🧩 Open-source solutions</strong>
              <p className="text-xs mt-1">Use open-source apps, frameworks or ghost app to launch instantly.</p>
            </div>
            <div className="border p-3 rounded">
              <strong>🔌 Try APIs</strong>
              <p className="text-xs mt-1">Explore our advanced API for instant data retrieval.</p>
            </div>
            <div className="border p-3 rounded">
              <strong>💬 Help & Support</strong>
              <p className="text-xs mt-1">Check our Developer Portal or chat with us to get guidance.</p>
            </div>
            <button className="text-blue-600 text-xs underline block text-center">Dismiss this onboarding screen</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Management;
