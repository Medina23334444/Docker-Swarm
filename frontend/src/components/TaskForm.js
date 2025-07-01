// src/components/TaskForm.js
import React, {useState, useEffect} from 'react';
import api from '../api';

const defaultForm = {
    title: '',
    description: '',
    priority: 'baja',
    due_date: ''
};

function TaskForm({editing, onSaved, cancelEdit}) {
    const [form, setForm] = useState(defaultForm);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (editing) {
            setForm({
                title: editing.title,
                description: editing.description || '',
                priority: editing.priority,
                // Cortamos a YYYY-MM-DD para el input, como antes
                due_date: editing.due_date.slice(0, 10)
            });
        } else {
            setForm(defaultForm);
        }
    }, [editing]);

    const handleChange = e => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleSubmit = async e => {
        e.preventDefault();
        // validaciones básicas
        if (!form.title.trim()) {
            alert('El título no puede estar vacío');
            return;
        }
        if (!form.due_date) {
            alert('Debes seleccionar una fecha válida');
            return;
        }

        setSaving(true);
        try {
            // **Toggle aplicado**: convertimos a Date antes de enviar
            const payload = {
                ...form,
                due_date: new Date(form.due_date)
            };

            if (editing) {
                await api.put(`/tasks/${editing.id}`, payload);
            } else {
                await api.post('/tasks', payload);
            }

            onSaved();
            setForm(defaultForm);
        } catch (err) {
            alert(
                err.response?.data?.detail ??
                err.response?.data ??
                'Error al guardar'
            );
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="container">
            <h2>{editing ? 'Editar Tarea' : 'Nueva Tarea'}</h2>
            <form onSubmit={handleSubmit}>
                {/* TÍTULO */}
                <div className="form-group">
                    <label>Título</label>
                    <input
                        className="form-control"
                        name="title"
                        value={form.title}
                        onChange={handleChange}
                        required
                    />
                </div>

                {/* DESCRIPCIÓN */}
                <div className="form-group">
                    <label>Descripción</label>
                    <textarea
                        className="form-control"
                        name="description"
                        value={form.description}
                        onChange={handleChange}
                    />
                </div>

                {/* PRIORIDAD */}
                <div className="form-group">
                    <label>Prioridad</label>
                    <select
                        className="form-control"
                        name="priority"
                        value={form.priority}
                        onChange={handleChange}
                    >
                        <option value="baja">Baja</option>
                        <option value="media">Media</option>
                        <option value="alta">Alta</option>
                    </select>
                </div>

                {/* FECHA LÍMITE */}
                <div className="form-group">
                    <label>Fecha Límite</label>
                    <input
                        className="form-control"
                        type="date"
                        name="due_date"
                        value={form.due_date}
                        onChange={handleChange}
                        required
                    />
                </div>

                {/* BOTONES */}
                <button type="submit" disabled={saving}>
                    {saving
                        ? 'Guardando...'
                        : editing
                            ? 'Actualizar'
                            : 'Crear'}
                </button>
                {editing && (
                    <button
                        type="button"
                        onClick={cancelEdit}
                        disabled={saving}
                    >
                        Cancelar
                    </button>
                )}
            </form>
        </div>
    );
}

export default TaskForm;
