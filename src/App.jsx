import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import UploadPage from './components/UploadPage';
import ResultPage from './components/ResultPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer'; // Add this line

export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/result" element={<ResultPage />} />
          </Routes>
        </div>
        <Footer /> {/* Add this line */}
      </div>
    </Router>
  );
}
