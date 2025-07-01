// src/pages/Profile.js
import React, { useEffect, useState } from 'react';
import api from '../api';

function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    api.get('/users/me')
       .then(res => setUser(res.data))
       .catch(() => setUser({ error: 'No se pudo cargar el perfil' }));
  }, []);

  if (!user) {
    return (
      <div className="container">
        <p>Cargando perfil…</p>
      </div>
    );
  }

  if (user.error) {
    return (
      <div className="container">
        <p style={{ color: 'red' }}>{user.error}</p>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Perfil de Usuario</h2>
      <div className="task-card">
        <div className="form-group">
          <label>ID:</label>
          <p>{user.id}</p>
        </div>
        <div className="form-group">
          <label>Usuario:</label>
          <p>{user.username}</p>
        </div>
      </div>
    </div>
  );
}

export default Profile;

