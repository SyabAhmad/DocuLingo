// File: pages/ResultPage.jsx
import React from 'react';

export default function ResultPage() {
  return (
    <div className="flex items-start justify-center min-h-[70vh] bg-gradient-to-br from-white to-indigo-50 py-10">
      <aside className="bg-white rounded-2xl shadow-lg p-6 max-w-xs w-full mr-8">
        <h3 className="text-lg font-bold text-indigo-700 mb-4">Original Document</h3>
        <div className="text-gray-600 text-sm h-64 overflow-y-auto border rounded p-2 bg-gray-50">
          {/* Replace with actual document preview */}
          <p>[Document preview here]</p>
        </div>
      </aside>
      <main className="bg-white rounded-2xl shadow-lg p-10 max-w-lg w-full flex flex-col items-center">
        <span className="text-4xl mb-4 text-indigo-500">🌐</span>
        <h3 className="text-xl font-bold text-indigo-700 mb-2">Translated Document</h3>
        <div className="text-gray-700 text-base h-64 overflow-y-auto border rounded p-4 bg-gray-50 w-full">
          {/* Replace with actual translation */}
          <p>Translated document preview will appear here soon...</p>
        </div>
      </main>
    </div>
  );
}
