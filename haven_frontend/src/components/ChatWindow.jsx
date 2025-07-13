import React from 'react';
import './ChatWindow.css';

const ChatWindow = ({ messages }) => {
  return (
    <div className="chat-window">
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.sender}`}>
          <div className="message-content">
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;
