from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import copy

router = APIRouter()

# Banco de dados original
BASE_PROFILES = {
    "1": {"id": "1", "name": "Alice", "email": "alice@example.com", "is_admin": False},
    "2": {"id": "2", "name": "Bob", "email": "bob@example.com", "is_admin": False},
}

class ProfileUpdate(BaseModel):
    name: str
    email: str
    is_admin: bool = False  # ⚠️ campo sensível

@router.put("/users/{user_id}")
def update_user_profile(user_id: str, data: ProfileUpdate, request: Request):
    current_user_id = request.headers.get("X-User-ID")
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    # 🔁 Clona os dados do "banco" a cada requisição
    fake_profiles = copy.deepcopy(BASE_PROFILES)

    if user_id not in fake_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    if secure_mode:
        # ✅ Atualiza apenas os campos seguros
        fake_profiles[user_id]["name"] = data.name
        fake_profiles[user_id]["email"] = data.email
    else:
        # ❌ Atualiza todos os campos, inclusive is_admin
        fake_profiles[user_id].update(data.dict())

    return fake_profiles[user_id]
