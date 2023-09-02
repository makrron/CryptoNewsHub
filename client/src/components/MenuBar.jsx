// MenuBar.jsx

import React from 'react';
import { Link } from 'react-router-dom';

export function MenuBar() {
  return (
    <div className="fixed inset-x-0 top-0 h-16 bg-black bg-opacity-50 backdrop-blur p-4 text-white z-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold">
            <Link to="/" className="transition duration-300 ease-in-out transform hover:scale-110 bg-yellow-600 hover:bg-yellow-300 text-black px-4 py-2 rounded-md shadow-md">
              CryptoNews
            </Link>
          </h1>
          <div className="space-x-4">
            <Link to="/news" className="transition duration-300 ease-in-out transform hover:scale-110 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md shadow-md">
              News
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
