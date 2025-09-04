// src/components/UserActionsDropdown.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

interface Props {
  userId: string;
}

const UserActionsDropdown: React.FC<Props> = ({ userId }) => {
  const navigate = useNavigate();

  return (
    <div className="absolute right-0 mt-1 w-48 bg-white shadow-lg border rounded z-50">
      <button
        className="w-full px-4 py-2 text-left hover:bg-gray-100"
        onClick={() => navigate(`/users/profiles/${userId}`)}
      >
        🔍 View Profile
      </button>
      <button
        className="w-full px-4 py-2 text-left hover:bg-gray-100"
        onClick={() => alert(`Change group for ${userId}`)}
      >
        👤 Change Group
      </button>
      <button
        className="w-full px-4 py-2 text-left hover:bg-gray-100"
        onClick={() => alert(`Deactivate user ${userId}`)}
      >
        ⏻ Deactivate User
      </button>
      <button
        className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-100"
        onClick={() => alert(`Delete user ${userId}`)}
      >
        🗑 Delete User
      </button>
    </div>
  );
};

export default UserActionsDropdown;
