// src/components/ProfileCard.tsx
import React from 'react';

const ProfileCard = () => {
  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-gray-200" />
          <div>
            <h2 className="text-lg font-semibold">Unknown</h2>
            <div className="flex items-center gap-2 text-sm text-green-600">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Active
            </div>
          </div>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          New Driver Profile
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-y-3 text-sm text-gray-700">
        <div>
          <span className="text-gray-400">Email</span>
          <div>Unknown</div>
        </div>
        <div>
          <span className="text-gray-400">Phone</span>
          <div>Unknown</div>
        </div>
        <div>
          <span className="text-gray-400">Client ID</span>
          <div className="text-green-500">No data</div>
        </div>
        <div>
          <span className="text-gray-400">User ID</span>
          <div className="flex items-center gap-2">
            622ccc22-efd9...
            <button className="text-gray-400 hover:text-gray-600 text-xs">📋</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;
