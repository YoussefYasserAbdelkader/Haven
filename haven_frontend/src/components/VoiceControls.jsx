import React from 'react';

export default function VoiceControls({ isRecording, onStart, onStop }) {
  return (
    <div className="voice-controls">
      {isRecording ? (
        <button onClick={onStop} className="stop-button">
          🎙️ Stop Listening
        </button>
      ) : (
        <button onClick={onStart} className="start-button">
          🎤 Start Talking
        </button>
      )}
    </div>
  );
}
