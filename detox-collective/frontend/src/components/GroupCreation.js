import React, { useState } from 'react';

export default function GroupCreation() {
  const [groupName, setGroupName] = useState('Demo Group');
  const [duration, setDuration] = useState(60);
  const [members, setMembers] = useState([]);
  const [memberEmail, setMemberEmail] = useState('');

  const addMember = (email) => {
    if (!email) return;
    if (!members.includes(email)) setMembers([...members, email]);
    setMemberEmail('');
  };

  const createGroup = async () => {
    // This demo does not call backend; implement POST /api/groups in production
    alert(`Group "${groupName}" with ${members.length} members created (demo)`);
  };

  return (
    <div style={{ padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
      <h2>Create Detox Group</h2>
      <input value={groupName} onChange={(e) => setGroupName(e.target.value)} />
      <div>
        <label>Duration (minutes)</label>
        <input type="number" value={duration} onChange={(e) => setDuration(Number(e.target.value))} />
      </div>
      <div>
        <input value={memberEmail} onChange={(e) => setMemberEmail(e.target.value)} placeholder="member@example.com" />
        <button onClick={() => addMember(memberEmail)}>Add</button>
      </div>
      <div>
        {members.map((m, i) => (
          <div key={i}>{m}</div>
        ))}
      </div>
      <button onClick={createGroup}>Create Group (demo)</button>
    </div>
  );
}
