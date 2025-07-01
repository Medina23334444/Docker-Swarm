// src/components/TaskList.js
import React, { useEffect, useState } from 'react';
import api from '../api';

function TaskList({ onEdit }) {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    const res = await api.get('/tasks');
    setTasks(res.data.tasks);
  };

  useEffect(() => { fetchTasks(); }, []);

  const toggleComplete = async (task) => {
    await api.put(`/tasks/${task.id}`, { completed: !task.completed });
    fetchTasks();
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Eliminar tarea?')) {
      await api.delete(`/tasks/${id}`);
      fetchTasks();
    }
  };

  return (
    <div className="container">
      <h2>Mis Tareas</h2>
      {tasks.map(t => (
        <div key={t.id} className="task-card">
          <div className="task-header">
            <strong>{t.title}</strong>
            <span>{new Date(t.due_date).toLocaleDateString()}</span>
          </div>
          <p>{t.description}</p>
          <div>
            <span>Prioridad: {t.priority}</span> — {t.completed ? '✓ Completada' : 'Pendiente'}
          </div>
          <div className="task-actions">
            <button onClick={() => toggleComplete(t)}>Toggle</button>
            <button onClick={() => onEdit(t)}>Editar</button>
            <button onClick={() => handleDelete(t.id)}>Eliminar</button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskList;
