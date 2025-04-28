from fastapi import APIRouter, Request, HTTPException
from typing import List

router = APIRouter()

# Simulação de um banco com muitos itens
BIG_DATASET = [{"id": i, "value": f"Item {i}"} for i in range(1, 10001)]  # 10 mil itens

@router.get("/items")
def get_items(request: Request, skip: int = 0, limit: int = 10000):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if secure_mode:
        # ✅ Versão segura — impõe limite máximo de 100 por requisição
        if limit > 100:
            raise HTTPException(status_code=400, detail="Limit exceeded: max is 100")
    
    # ❌ Versão vulnerável — retorna tudo se solicitado
    return BIG_DATASET[skip : skip + limit]
