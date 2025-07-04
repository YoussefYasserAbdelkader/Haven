import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [messages, setMessages] = useState([]);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const playReplyAudio = (audioUrl) => {
    if (!audioUrl) return;
    const audio = new Audio(audioUrl);
    audio.play().catch((e) => {
      console.error("Reply audio playback failed:", e);
    });
  };

  const startRecording = async () => {
    if (isProcessing) return;
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    chunksRef.current = [];
    mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
    mediaRecorder.onstop = async () => {
      setIsRecording(false);
      setIsProcessing(true);
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob, 'user_audio.webm');

      const response = await fetch('http://localhost:3000/start', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.user_text) {
        setMessages((prev) => [...prev, { role: 'user', content: data.user_text }]);
      }
      if (data.reply) {
        setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
      }
      if (data.audio_url) {
        playReplyAudio(data.audio_url);
      }
      setIsProcessing(false);
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
    }
  };

  return (
    <div className="App">
      <h1>Haven – Your Voice Therapist</h1>
      <button
        onMouseDown={startRecording}
        onMouseUp={stopRecording}
        onTouchStart={startRecording}
        onTouchEnd={stopRecording}
        disabled={isProcessing}
        style={{
          background: isRecording ? '#4caf50' : '#2196f3',
          color: 'white',
          fontSize: '1.2em',
          padding: '1em 2em',
          borderRadius: '2em',
          border: 'none',
          cursor: isProcessing ? 'not-allowed' : 'pointer'
        }}
      >
        {isRecording ? '🎙️ Recording... Release to send' : isProcessing ? '🤖 Thinking...' : '🎤 Hold to talk'}
      </button>

      <div className="chat-log">
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.role === 'user' ? 'You' : 'Haven'}:</strong> {msg.content}
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;
