<<<<<<< HEAD
// src/components/Header.tsx
import { Bell, User } from "lucide-react";

const Header = () => {
  return (
    <header className="xl:bg-gray-150 flex 2xl:py-[12px]   ">
      <div
        className="
         mb-4 grid   w-full h-[80px]
    md:h-[102px]
    xl:h-[120px]
    2xl:h-[102px]
    max-w-[1081px] 
    xl:max-w-[1200px] 2xl:max-w-[1830px]  
    md:mt-[40px] md:mx-[32px] md:my-[24px] md:py-[12px]
    mx-auto bg-gray-800 border-rounded-lg 
    2xl:mx-[32px] 2xl:my-[20px] md:py-[12px] rounded-full 
    2xl:bg-white xl:bg-white shadow-sm
      "
      >
        <div className="flex items-center justify-between 2xl:mx-[36px] 2xl:my-[4px] md:mx-[36px] xl:my-[8px] ">
          <div>
            <p className="text-[16px] font-light  text-gray-500  ">
              Good Morning,
            </p>
            <h1 className="text-[20px] font-bold text-gray-800">Atharva D</h1>
          </div>

          <div className="flex items-center gap-4">
            {/* Notification Bell */}
            <button className="relative p-[15px] rounded-full hover:bg-gray-300">
              {/* Red Dot Ping */}
              {/* <span className="absolute top-1 right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span> */}

              <Bell className="w-[24px] h-[24px] text-gray-600" />
            </button>

            {/* Avatar */}
            <button className="relative p-2 rounded-full hover:bg-gray-100">
              <div className="w-10 h-10 rounded-full bg-violet-200 flex items-center justify-center text-lg">
                <span role="img" aria-label="avatar">
                  🧑‍💼
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
=======
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
>>>>>>> feature/trip-graph-api
