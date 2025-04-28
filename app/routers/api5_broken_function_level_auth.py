from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

# Simulação de perfis de usuário
fake_roles = {
    "1": "admin",   # Alice
    "2": "user",    # Bob
}

@router.delete("/admin/delete-user/{target_user_id}")
def delete_user(target_user_id: str, request: Request):
    current_user_id = request.headers.get("X-User-ID")
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if not current_user_id or current_user_id not in fake_roles:
        raise HTTPException(status_code=401, detail="Invalid or missing user ID")

    if secure_mode:
        # ✅ Apenas usuários com perfil admin podem executar
        if fake_roles[current_user_id] != "admin":
            raise HTTPException(status_code=403, detail="Access denied: not an admin")

    # ❌ Qualquer usuário autenticado (ou nem isso) pode deletar
    return {"message": f"User {target_user_id} has been deleted (simulation)"}
