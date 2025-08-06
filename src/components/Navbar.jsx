// File: components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <header className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-lg rounded-b-2xl">
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center text-2xl font-extrabold text-white tracking-wide drop-shadow">
          <span className="mr-3 text-3xl">📝</span> DocuLingo
        </Link>
        <ul className="flex space-x-8 text-white font-semibold">
          <li>
            <Link to="/" className="hover:underline underline-offset-8">Home</Link>
          </li>
          <li>
            <Link to="/upload" className="hover:underline underline-offset-8">Translate</Link>
          </li>
          <li>
            <Link to="/result" className="hover:underline underline-offset-8">Result</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
