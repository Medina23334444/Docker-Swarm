from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


# --- Usuarios ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Tareas ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    due_date: date


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: str
    due_date: date
    completed: bool
    owner_id: str


# Para respuestas con listas
class TaskList(BaseModel):
    tasks: List[TaskOut]
