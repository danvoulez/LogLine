from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict, Any
import hmac
import hashlib
from loguru import logger

from app.core.settings import settings

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    responses={
        400: {"description": "Assinatura ausente ou JSON inválido"},
        401: {"description": "Assinatura inválida"},
        200: {"description": "Webhook recebido com sucesso"},
    }
)

@router.post(
    "/receive",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Recebe webhooks externos autenticados por HMAC"
)
async def receive_webhook(request: Request) -> Dict[str, Any]:
    """
    Endpoint genérico para receber webhooks externos com autenticação HMAC.
    
    - Verifica HMAC-SHA256 usando JWT_SECRET.
    - Loga payload recebido e devolve status apropriado.
    - Gera logs estruturados para auditoria.

    Exemplos de resposta:
    - 200: {"status": "received", "event": "event_name"}
    - 400: {"detail": "Signature missing"}
    - 401: {"detail": "Invalid signature"}
    """
    SECRET = settings.JWT_SECRET.get_secret_value().encode()
    signature = request.headers.get("X-Hub-Signature-256")
    body = await request.body()

    if not signature:
        logger.warning("webhook.receive | missing signature | ip=%s", request.client.host if request.client else "unknown")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature missing")

    mac = hmac.new(SECRET, body, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    if not hmac.compare_digest(expected, signature):
        logger.warning("webhook.receive | invalid signature | ip=%s | signature=%s", request.client.host if request.client else "unknown", signature)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception as exc:
        logger.error("webhook.receive | invalid JSON | exc=%s | ip=%s", exc, request.client.host if request.client else "unknown")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")

    event = payload.get("event", "<unknown>")
    logger.info("webhook.receive | event=%s | ip=%s | payload=%s", event, request.client.host if request.client else "unknown", payload)
    # Pontos para: enfileirar processamento, trigger de fluxo, etc.

    return {"status": "received", "event": event}