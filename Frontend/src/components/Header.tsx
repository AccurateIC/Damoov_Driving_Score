// src/components/Header.tsx
import { Bell, User } from 'lucide-react';

const Header = () => {
  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-gray-200 bg-white shadow-sm sticky top-0 z-40">
      <h1 className="text-lg font-semibold text-gray-800">DataHub Dashboard</h1>
      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-full hover:bg-gray-100">
          <Bell className="w-5 h-5 text-gray-700" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-ping"></span>
        </button>
        <div className="flex items-center gap-2">
          <User className="w-5 h-5 text-gray-700" />
          <span className="text-sm text-gray-700">Admin</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
