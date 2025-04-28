from fastapi import APIRouter, Request, HTTPException
import requests
from urllib.parse import urlparse

router = APIRouter()

@router.get("/fetch-url")
def fetch_url(target_url: str, request: Request):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if secure_mode:
        # ✅ Validação: bloqueia IPs locais e domínios perigosos
        parsed_url = urlparse(target_url)
        hostname = parsed_url.hostname

        if not hostname:
            raise HTTPException(status_code=400, detail="Invalid URL")

        # Lista de hostnames proibidos (simples)
        forbidden_hostnames = ["localhost", "127.0.0.1", "0.0.0.0"]

        if hostname in forbidden_hostnames:
            raise HTTPException(status_code=400, detail="Access to internal resources forbidden")

    try:
        response = requests.get(target_url, timeout=5, verify=False)  #response = requests.get(target_url, timeout=5)
        return {"status_code": response.status_code, "content": response.text[:200]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")
