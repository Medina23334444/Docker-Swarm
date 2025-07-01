# app/main.py

import os
import threading
from concurrent.futures import ThreadPoolExecutor

import motor.frameworks.asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.routers import users, tasks

# 1) Reduce el stack de cada hilo a 1 MiB
threading.stack_size(1 << 20)
# 2) Limita el ThreadPoolExecutor de Motor a 4 hilos
motor.frameworks.asyncio._EXECUTOR = ThreadPoolExecutor(max_workers=4)

app = FastAPI(
    title="Task Manager API",
    description="API de gestión de tareas con usuarios, roles, JWT y MongoDB"
)

# 3) Configuración CORS
origins = [
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://frontend:3000",
    "http://192.168.99.114:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4) Registro de routers
app.include_router(users.router)
app.include_router(tasks.router)

# 5) URI de MongoDB
LOCAL_URI = "mongodb://mongo:27017/taskmanager"
RS_URI = "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/taskmanager?replicaSet=rs0"
MONGO_URI = os.getenv("MONGO_URI", LOCAL_URI)
if os.getenv("ENV") == "swarm":
    MONGO_URI = RS_URI


# 6) Conectar / cerrar Mongo en eventos
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.db = app.mongodb_client.get_default_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
def root():
    return {"message": "Task Manager API running"}
