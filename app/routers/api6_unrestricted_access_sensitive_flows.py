from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

# Simulação de pedidos
fake_orders = {
    "1001": {"order_id": "1001", "status": "pending", "user_id": "1"},
    "1002": {"order_id": "1002", "status": "pending", "user_id": "2"},
}

@router.post("/orders/{order_id}/complete")
def complete_order(order_id: str, request: Request):
    current_user_id = request.headers.get("X-User-ID")
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if order_id not in fake_orders:
        raise HTTPException(status_code=404, detail="Order not found")

    if secure_mode:
        # ✅ Verifica se o usuário é o dono do pedido
        if not current_user_id or current_user_id != fake_orders[order_id]["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied: not your order")
    
    # ❌ Permite qualquer um completar qualquer pedido
    fake_orders[order_id]["status"] = "completed"
    return {"message": f"Order {order_id} marked as completed"}
