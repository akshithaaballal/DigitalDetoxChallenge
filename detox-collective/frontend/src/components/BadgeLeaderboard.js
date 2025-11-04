import React from 'react';

export default function BadgeLeaderboard({ members = [] }) {
  return (
    <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
      <h2>Leaderboard</h2>
      <ul>
        {members.length === 0 && <li>No data (demo)</li>}
        {members.map((m, i) => (
          <li key={i}>#{i + 1} {m.userId} — {m.credits} credits</li>
        ))}
      </ul>
    </div>
  );
}
