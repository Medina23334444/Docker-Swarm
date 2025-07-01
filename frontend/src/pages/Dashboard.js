import React, { useState } from 'react';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';

function Dashboard() {
  const [editing, setEditing] = useState(null);
  const refresh = () => setEditing(null);

  return (
    <div>
      <TaskForm editing={editing} onSaved={refresh} cancelEdit={() => setEditing(null)} />
      <TaskList onEdit={setEditing} />
    </div>
  );
}

export default Dashboard;
