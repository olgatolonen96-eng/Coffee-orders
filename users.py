from fastapi import APIRouter, HTTPException
from auth import create_access_token, hash_password, verify_password
from models import UserLogin, UserPublic, UserRegister, UserRole
from storage import load_data, save_data

router = APIRouter(prefix="/auth", tags=["auth"])

USERS_FILE = "users.json"

@router.post("/register", response_model=UserPublic)
def register(data: UserRegister):
    users = load_data(USERS_FILE, default=[])

    if any(u["email"] == data.email for u in users):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_id = max((u["id"] for u in users), default=0) + 1

    new_user = {
        "id": new_id,
        "name": data.name,
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "role": UserRole.customer.value,
    }
    users.append(new_user)
    save_data(USERS_FILE, users)

    return UserPublic(
        id=new_id, name=new_user["name"], email=new_user["email"], role=new_user["role"]
    )


@router.post("/login")
def login(data: UserLogin):
    users = load_data(USERS_FILE, default=[])
    user = next((u for u in users if u["email"] == data.email), None)

    if user is None or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token = create_access_token(user_id=user["id"], role=user["role"])
    return dict(access_token=token, token_type="bearer")