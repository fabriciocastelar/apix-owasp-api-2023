from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/public/info")
def public_info():
    return {"info": "This is public information"}

@router.get("/internal/config")
def internal_config(request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if secure_mode:
        # ✅ Em modo seguro, bloqueia acesso direto a rota interna
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        # ❌ Em modo inseguro, expõe informações internas
        return {
            "database_password": "super_secret_db_password",
            "feature_flags": {"beta_mode": True, "new_ui": False},
            "debug_mode": True
        }

@router.get("/v1/legacy-endpoint")
def legacy_endpoint(request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if secure_mode:
        # ✅ Em modo seguro, bloqueia acesso a APIs antigas
        raise HTTPException(status_code=410, detail="This API version is deprecated")
    else:
        # ❌ Permite uso de API obsoleta
        return {"message": "Deprecated data served from v1"}
