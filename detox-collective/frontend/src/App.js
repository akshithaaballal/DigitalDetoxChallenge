import React from 'react';
import GroupCreation from './components/GroupCreation';
import DetoxTimer from './components/DetoxTimer';

export default function App() {
  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h1>Detox Collective — Demo</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <GroupCreation />
        <DetoxTimer groupId={'demo-group'} sessionId={'demo-session'} detoxDuration={1} />
      </div>
    </div>
  );
}
