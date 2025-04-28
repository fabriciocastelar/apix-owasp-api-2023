from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

# Simulando banco de dados em memória
fake_users_db = {
    "1": {"id": "1", "name": "Alice", "email": "alice@example.com"},
    "2": {"id": "2", "name": "Bob", "email": "bob@example.com"},
}

@router.get("/users/{user_id}")
def get_user_data(user_id: str, request: Request):
    current_user_id = request.headers.get("X-User-ID")
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")

    if secure_mode:
        # ✅ Versão segura
        if user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Access forbidden: not your data")

    # ❌ Versão vulnerável (sem checagem de identidade)
    return fake_users_db[user_id]
