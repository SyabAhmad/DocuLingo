// File: pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center text-center py-20 px-6 bg-gradient-to-br from-indigo-50 to-white min-h-[80vh]">
      <div className="bg-white rounded-2xl shadow-lg p-10 max-w-xl w-full">
        <h1 className="text-4xl font-bold text-indigo-700 mb-4">Welcome to DocuLingo</h1>
        <p className="text-lg text-gray-600 mb-6">
          AI-powered translation for educational documents.<br />Just upload and we’ll do the magic.
        </p>
        <Link to="/upload" className="px-8 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 transition font-semibold shadow">
          Start Translating
        </Link>
      </div>
    </div>
  );
}
