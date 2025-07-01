from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from app.models import TaskCreate, TaskUpdate, TaskOut, TaskList, id_to_str, get_db
from app.routers.users import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskCreate,
        current_user: Any = Depends(get_current_user),
        db: AsyncIOMotorDatabase = Depends(get_db),
) -> Any:
    # Convierte el Pydantic model a dict serializable
    doc = jsonable_encoder(task)
    # Asigna el owner y marca como no completada
    doc["owner_id"] = str(current_user.get("_id"))
    doc["completed"] = False
    # Inserta en Mongo
    res = await db["tasks"].insert_one(doc)
    # Recupera el documento recién creado
    created = await db["tasks"].find_one({"_id": res.inserted_id})
    # Convierte _id → id y retorna
    return id_to_str(created)


@router.get("", response_model=TaskList)
async def list_tasks(
        current_user: Any = Depends(get_current_user),
        db: AsyncIOMotorDatabase = Depends(get_db),
) -> Any:
    cursor = db["tasks"].find({"owner_id": str(current_user.get("_id"))})
    docs = [id_to_str(doc) async for doc in cursor]
    return TaskList(tasks=docs)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
        task_id: str,
        current_user: Any = Depends(get_current_user),
        db: AsyncIOMotorDatabase = Depends(get_db),
) -> Any:
    doc = await db["tasks"].find_one({
        "_id": ObjectId(task_id),
        "owner_id": str(current_user.get("_id"))
    })
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return id_to_str(doc)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
        task_id: str,
        task: TaskUpdate,
        current_user: Any = Depends(get_current_user),
        db: AsyncIOMotorDatabase = Depends(get_db),
) -> Any:
    update_data = {k: v for k, v in task.dict(exclude_unset=True).items()}
    result = await db["tasks"].update_one(
        {"_id": ObjectId(task_id), "owner_id": str(current_user.get("_id"))},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or no change")
    doc = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    return id_to_str(doc)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: str,
        current_user: Any = Depends(get_current_user),
        db: AsyncIOMotorDatabase = Depends(get_db),
) -> None:
    result = await db["tasks"].delete_one({
        "_id": ObjectId(task_id),
        "owner_id": str(current_user.get("_id"))
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
