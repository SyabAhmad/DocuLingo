// File: pages/UploadPage.jsx
import React, { useState } from 'react';

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'ar', label: 'Arabic' },
  { code: 'fr', label: 'French' },
  { code: 'es', label: 'Spanish' },
  { code: 'de', label: 'German' },
  { code: 'zh', label: 'Chinese' },
  { code: 'hi', label: 'Hindi' },
  // Add more as needed
];

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [outputFormat, setOutputFormat] = useState('image');
  const [targetLang, setTargetLang] = useState('en');

  const handleUpload = (e) => {
    const uploaded = e.target.files[0];
    setFile(uploaded);
    setResult(null);
    setError('');
  };

  const handleTranslate = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_lang', targetLang);
    formData.append('output_format', outputFormat);

    try {
      const response = await fetch('http://localhost:5000/api/translate', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Translation failed');
      // For file download, handle as blob
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setResult(url);
    } catch (err) {
      setError('Failed to translate document.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] bg-gradient-to-br from-white to-indigo-50">
      <div className="bg-white rounded-2xl shadow-lg p-10 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-indigo-700">Upload Educational Document</h2>
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-indigo-300 rounded-xl p-6 mb-4 cursor-pointer hover:border-indigo-500 transition">
          <span className="mb-2 text-gray-500">Click or drag file to upload</span>
          <input
            type="file"
            accept="application/pdf, image/*"
            onChange={handleUpload}
            className="hidden"
          />
        </label>
        <div className="mb-4 flex gap-4">
          <div>
            <label className="mr-2 font-medium">Output:</label>
            <select
              value={outputFormat}
              onChange={e => setOutputFormat(e.target.value)}
              className="border rounded px-2 py-1"
            >
              <option value="image">Image</option>
              <option value="pdf">PDF</option>
            </select>
          </div>
          <div>
            <label className="mr-2 font-medium">Language:</label>
            <select
              value={targetLang}
              onChange={e => setTargetLang(e.target.value)}
              className="border rounded px-2 py-1"
            >
              {LANGUAGES.map(lang => (
                <option key={lang.code} value={lang.code}>{lang.label}</option>
              ))}
            </select>
          </div>
        </div>
        {file && (
          <p className="text-green-600 mb-2">Uploaded: {file.name}</p>
        )}
        <button
          className="w-full mt-4 px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 transition font-semibold shadow"
          onClick={handleTranslate}
          disabled={loading}
        >
          {loading ? 'Translating...' : 'Translate Now'}
        </button>
        {error && <p className="text-red-600 mt-4">{error}</p>}
        {result && (
          <div className="mt-6 text-left text-sm text-gray-700">
            <a href={result} download={`translated.${outputFormat === 'pdf' ? 'pdf' : 'png'}`} className="text-indigo-600 underline">
              Download Translated {outputFormat.toUpperCase()}
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
