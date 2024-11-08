import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState(null);
  const [rate, setRate] = useState(1.0);  // Default rate
  const [volume, setVolume] = useState(1.0);  // Default volume
  const [language, setLanguage] = useState('en');  // Default language

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Send POST request with text and settings (rate, volume, language)
      const response = await axios.post(
        'http://localhost:8000/api/', // API endpoint for TTS
        { text, rate, volume, lang: language },
        { responseType: 'blob' } // Expecting binary data (audio) in response
      );

      // Create a URL for the audio blob to allow playback and download
      const audioBlob = new Blob([response.data], { type: 'audio/mp3' });
      setAudioUrl(URL.createObjectURL(audioBlob));
    } catch (error) {
      console.error('Error generating speech:', error);
    }
  };

  return (
    <div className="App">
      <h1>Text to Speech Converter</h1>

      {/* Form to input text and submit for conversion */}
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text here"
        />
        <div>
          <label>Rate: </label>
          <input
            type="range"
            min="0.1"
            max="2.0"
            step="0.1"
            value={rate}
            onChange={(e) => setRate(e.target.value)}
          />
          <span>{rate}</span>
        </div>

        <div>
          <label>Volume: </label>
          <input
            type="range"
            min="0.0"
            max="10.0"
            step="1"
            value={volume}
            onChange={(e) => setVolume(e.target.value)}
          />
          <span>{volume}</span>
        </div>

        <div>
          <label>Language: </label>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            {/* Add more languages if needed */}
          </select>
        </div>

        <button type="submit">Convert to Speech</button>
      </form>

      {/* Display audio player and download link if audioUrl is available */}
      {audioUrl && (
        <div className="audio-container">
          <audio controls src={audioUrl}></audio>
          <a href={audioUrl} download="output.mp3">Download Audio</a>
        </div>
      )}
    </div>
  );
}

export default App;
