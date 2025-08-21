import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [xmlPreview, setXmlPreview] = useState(null);

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);
    setXmlPreview(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/convert-pdf-to-xml`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during conversion');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.xml_file) return;

    try {
      const response = await axios.get(
        `${API_BASE_URL}/download/${result.xml_file}`,
        { responseType: 'blob' }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', result.xml_file);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download file');
    }
  };

  const handlePreview = async () => {
    if (!result?.xml_file) return;

    try {
      const response = await axios.get(
        `${API_BASE_URL}/preview/${result.xml_file}`
      );
      setXmlPreview(response.data.xml_content);
    } catch (err) {
      setError('Failed to load preview');
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>PDF to XML Converter</h1>
        
        <div className="upload-section">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="file-input"
          />
          
          {file && (
            <div className="file-info">
              <p>Selected file: {file.name}</p>
              <p>Size: {(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}
          
          <button
            onClick={handleUpload}
            disabled={!file || isLoading}
            className="upload-btn"
          >
            {isLoading ? 'Converting...' : 'Convert to XML'}
          </button>
        </div>

        {error && (
          <div className="error">
            <p>Error: {error}</p>
          </div>
        )}

        {result && (
          <div className="result-section">
            <h3>Conversion Successful!</h3>
            <p>XML file generated: {result.xml_file}</p>
            
            <div className="action-buttons">
              <button onClick={handleDownload} className="download-btn">
                Download XML
              </button>
              <button onClick={handlePreview} className="preview-btn">
                Preview XML
              </button>
            </div>
          </div>
        )}

        {xmlPreview && (
          <div className="preview-section">
            <h3>XML Preview</h3>
            <pre className="xml-preview">
              {xmlPreview}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;