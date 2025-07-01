from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from fastapi import Request


# -----------------------------
#  Pydantic schemas for users
# -----------------------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------------
#  Pydantic schemas for tasks
# -----------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: str = Field(..., min_length=1)
    due_date: date


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: str
    due_date: date
    completed: bool
    owner_id: str


class TaskList(BaseModel):
    tasks: List[TaskOut]


# -----------------------------
#  Helpers
# -----------------------------

def id_to_str(doc: dict) -> dict:
    """
    Convierte el campo _id de Mongo a cadena y lo renombra a id.
    También convierte owner_id si existe.
    """
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    if "owner_id" in doc:
        doc["owner_id"] = str(doc["owner_id"])
    return doc


def get_db(request: Request):
    """
    Dependencia para obtener la base de datos del objeto FastAPI.
    """
    return request.app.db
