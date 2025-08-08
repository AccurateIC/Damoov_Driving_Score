// src/pages/DataTool.tsx
import React from 'react';

const DataTool = () => {
  const Section = ({ title, items }: { title: string; items: string[] }) => (
    <div className="flex-1 p-4 border-r last:border-r-0">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex justify-between text-sm text-gray-700">
            <span>{item}</span>
            <span className="text-gray-500">No Data</span>
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      <div>
        <h1 className="text-xl font-semibold text-gray-800">DataTool | Check User</h1>
        <p className="text-sm text-gray-500 mt-1">
          Check Telematics Data and User Permissions
        </p>
      </div>

      <div className="bg-white shadow rounded p-6 flex gap-6">
        <Section
          title="User"
          items={[
            'User ID',
            'Registration date',
            'Email',
            'Phone',
            'First Name',
            'Last Name',
            'Client ID',
            'Company',
            'Application',
            'User Group'
          ]}
        />

        <Section
          title="SDK"
          items={[
            'Tracks on device',
            'Latest Heartbeat Date (UTC)',
            'SDK version',
            'Tracking',
            'RealTime location',
            'Logging',
            'Invalid Tracks',
            'Insufficient Speed',
            'Insufficient Length',
            'Low Accuracy',
            'Wrong Dates',
            'Duplicated',
            'Other',
            'Raw Tracks',
            'Processed Tracks',
            'Excluded Tracks',
            'Enriched Tracks',
            'Latest Track Date (UTC)',
            'Latest Waypoint Latitude',
            'Latest Waypoint Longitude'
          ]}
        />

        <Section
          title="Device"
          items={['Device Model', 'Device OS version']}
        />

        <div className="flex-1 p-4">
          <h3 className="text-lg font-semibold mb-4">Status</h3>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex justify-between">
              <span className="text-green-700 underline cursor-pointer">Permissions Guide</span>
              <span className="text-xs border border-gray-400 px-2 py-0.5 rounded-full">NO DATA</span>
            </li>
            <li className="font-medium pt-2">App Permissions</li>
            {['GPS (Location)', 'Motion Activity (Android)', 'Motion Fitness (iOS)', 'Low Precise Location (iOS)'].map((item, i) => (
              <li key={i} className="flex justify-between text-gray-700">
                <span>{item}</span>
                <span className="text-gray-500">No Data</span>
              </li>
            ))}
            <li className="font-medium pt-2">Device Permissions</li>
            {['Wi-fi', 'GPS', 'Mobile Data', 'Low Power Mode', 'Device Was Hacked'].map((item, i) => (
              <li key={i} className="flex justify-between text-gray-700">
                <span>{item}</span>
                <span className="text-gray-500">No Data</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DataTool;
