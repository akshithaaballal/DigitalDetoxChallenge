import React, { useState, useEffect } from 'react';

export default function DetoxTimer({ groupId, sessionId, detoxDuration = 60 }) {
  const [timeLeft, setTimeLeft] = useState(detoxDuration * 60);
  const [isActive, setIsActive] = useState(false);
  const [userStatus, setUserStatus] = useState('pending');

  useEffect(() => {
    let interval = null;
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => setTimeLeft((t) => t - 1), 1000);
    } else if (timeLeft <= 0 && isActive) {
      setIsActive(false);
      setUserStatus('completed');
    }
    return () => clearInterval(interval);
  }, [isActive, timeLeft]);

  const startDetox = () => {
    setIsActive(true);
    setUserStatus('active');
    // call backend to create session in production
  };

  const breakContract = () => {
    setIsActive(false);
    setUserStatus('failed');
    // call backend to update session in production
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  return (
    <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
      <h2>Detox Timer</h2>
      <div style={{ fontSize: 36, fontFamily: 'monospace' }}>{formatTime(timeLeft)}</div>
      <div>Status: {userStatus}</div>
      {!isActive && userStatus === 'pending' && <button onClick={startDetox}>Start Detox</button>}
      {isActive && <button onClick={breakContract}>Break Contract</button>}
      {userStatus === 'completed' && <button disabled>✓ Completed</button>}
    </div>
  );
}
