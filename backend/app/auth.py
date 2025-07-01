import os
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt, JWTError


class AuthHandler:
    """
    Encapsula hashing de contraseñas y JWT.
    """
    security = HTTPBearer()
    secret = os.getenv("SECRET_KEY", "secret")
    algo = "HS256"
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    expire_minutes = 30

    def get_password_hash(self, plain: str) -> str:
        return self.pwd_ctx.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.pwd_ctx.verify(plain, hashed)

    def encode_token(self, user_id: str) -> str:
        payload: Dict = {
            "exp": datetime.utcnow() + timedelta(minutes=self.expire_minutes),
            "iat": datetime.utcnow(),
            "sub": str(user_id)
        }
        return jwt.encode(payload, self.secret, algorithm=self.algo)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algo])
            return payload["sub"]
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

    def auth_wrapper(self, creds: HTTPAuthorizationCredentials = Security(security)) -> str:
        return self.decode_token(creds.credentials)
