# Task Manager

Proyecto avanzado de gestión de tareas con backend en FastAPI, frontend en React, y base de datos MongoDB, todo dockerizado.

## Estructura
- **backend/**: API con FastAPI, autenticación JWT, MongoDB.
- **frontend/**: React, Axios, UI para gestionar tareas.
- **docker-compose.yml**: Orquesta todo.
- **mongo**: Contenedor MongoDB.

## ¿Cómo correr el proyecto?

1. Clona este repo:
    ```
    git clone <URL-del-zip-o-repo>
    cd task-manager
    ```

2. Levanta todo con docker-compose:
    ```
    docker-compose up --build
    ```

3. Accede a la app:
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger)

## Funcionalidades

- Registro/Login con JWT
- Roles de usuario (admin/usuario)
- CRUD de tareas: prioridad, fecha límite, estado, asignación de usuario
- UI amigable y responsiva

---

Si tienes dudas, abre un issue.
