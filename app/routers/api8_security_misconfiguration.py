from fastapi import APIRouter, Request, Response, HTTPException

router = APIRouter()

@router.get("/debug")
def debug_endpoint(request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if not secure_mode:
        # ❌ Modo inseguro: retorna detalhes internos
        return {
            "debug": True,
            "server_version": "FastAPI 0.100",
            "database_info": "PostgreSQL 13.3",
            "internal_ips": ["127.0.0.1", "10.0.0.5"]
        }
    else:
        # ✅ Modo seguro: responde genérico + adiciona headers de proteção
        response = Response(content='{"message": "Service operational"}', media_type="application/json")
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
