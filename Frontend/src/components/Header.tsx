// src/components/Header.tsx
import { Bell, User } from 'lucide-react';

const Header = () => {
  return (
    <header className='  md:mx-[32px]   '>
      <div className=" mb-4 md:w-[1081px] md:h-[102px] border-rounded-lg md:mt-[40px] md:mx-[32px] md:my-[24px] md:py-[12px] rounded-full bg-white shadow-sm  ">
       <div className='flex items-center justify-between md:mx-[36px] md:my-[8px] '>
         <div>
          <p className="text-[16px] font-light  text-gray-500  ">Good Morning,</p>
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
