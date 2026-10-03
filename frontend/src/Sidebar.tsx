import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="w-16 bg-white border-r border-[#E4E7EC] flex flex-col items-center py-6 gap-6">
      {/* 6 circle icons. 3rd is active. */}
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border-2 border-blue-500 p-0.5 flex items-center justify-center">
        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
      <Link to="/" className="w-4 h-4 rounded-full border border-gray-300">
      </Link>
    </div>
  );
};

export default Sidebar;
