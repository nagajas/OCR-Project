import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // Importing the CSS file

function App() {
  const [image, setImage] = useState(null);
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (event) => {
    setImage(event.target.files[0]);
    setText('');  
    setError(''); 
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!image) {
      setError('Please upload an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    try {
      setLoading(true);  // Set loading state to true
      console.log("Sending image to server...");
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log("Response received:", response.data);
      setText(response.data.text);
      setLoading(false);  // Set loading state to false
    } catch (err) {
      console.error("Error occurred:", err);
      setError('An error occurred while processing the image.');
      setLoading(false);  // Set loading state to false
    }
  };

  return (
    <div className="App">
      <h1>OCR Image Upload</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" accept="image/*" onChange={handleImageUpload} className="upload-input"/>
        <button type="submit" className="upload-button">Upload and Extract Text</button>
      </form>
      {loading ? (
        <div className="loading">
          <p>Loading...</p>
        </div>
      ) : (
        <>
          {error && <p className="error">{error}</p>}
          {text && (
            <div className="output">
              <h2>Extracted Text:</h2>
              <p>{text}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
