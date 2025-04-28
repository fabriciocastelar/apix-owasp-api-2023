from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Fake "banco de usuários"
users = {
    "alice": "1234",
    "bob": "abcd"
}

# Fake "tokens"
tokens = {
    "alice": "token-alice-123",
    "bob": "token-bob-abc"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest, request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if secure_mode:
        # ✅ Versão segura — verifica usuário e senha
        if data.username not in users or users[data.username] != data.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    else:
        # ❌ Versão vulnerável — qualquer login funciona
        pass

    # Gera token fake (para simplificação da demo)
    token = tokens.get(data.username, "token-anon")
    return {"token": token}

@router.get("/profile")
def get_profile(request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"
    token = request.headers.get("Authorization")

    if secure_mode:
        if token not in tokens.values():
            raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Retorna dados genéricos
    return {"message": "Access granted to protected profile data"}
