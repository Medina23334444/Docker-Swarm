# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from app.models import UserCreate, UserOut, Token, id_to_str, get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from bson import ObjectId
import os

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Secret para JWT (en producción, cargar desde variable de entorno segura)
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
        user: UserCreate,
        db: AsyncIOMotorDatabase = Depends(get_db)
) -> Any:
    existing = await db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    user_dict = user.dict()
    # Hashear la contraseña con Passlib (ejemplo comentado)
    # from passlib.context import CryptContext
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # hashed = pwd_context.hash(user_dict.pop("password"))
    # user_dict["hashed_password"] = hashed
    user_dict["hashed_password"] = user_dict.pop("password")
    result = await db["users"].insert_one(user_dict)
    doc = await db["users"].find_one({"_id": result.inserted_id})
    return id_to_str(doc)


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncIOMotorDatabase = Depends(get_db)
) -> Any:
    user = await db["users"].find_one({"username": form_data.username})
    if not user or form_data.password != user.get("hashed_password"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    to_encode = {"sub": str(user.get("_id"))}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncIOMotorDatabase = Depends(get_db)
) -> Any:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: Any = Depends(get_current_user)) -> Any:
    """Devuelve el usuario autenticado actual."""
    return id_to_str(current_user)
