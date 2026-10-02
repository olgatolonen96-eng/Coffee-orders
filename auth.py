from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from models import UserRole
from storage import load_data

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
TOKEN_LIFETIME_HOURS = 12

USERS_FILE = "users.json"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_LIFETIME_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
        )

    user_id = int(payload["sub"])
    users = load_data(USERS_FILE, default=[])
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return {"id": user["id"], "role": user["role"], "name": user["name"]}


def require_role(*allowed_roles: UserRole):
    allowed_values = [r.value for r in allowed_roles]

    def checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для этого действия",
            )
        return user

    return checker