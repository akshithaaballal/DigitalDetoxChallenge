import React, { useState } from 'react';

export default function GroupChat({ groupId }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const sendMessage = () => {
    if (!newMessage.trim()) return;
    setMessages([...messages, { text: newMessage, id: Date.now() }]);
    setNewMessage('');
  };

  return (
    <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
      <h2>Group Chat</h2>
      <div style={{ maxHeight: 200, overflow: 'auto', marginBottom: 8 }}>
        {messages.map((m) => (
          <div key={m.id}>{m.text}</div>
        ))}
      </div>
      <input value={newMessage} onChange={(e) => setNewMessage(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
