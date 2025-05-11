from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Any, Dict
import httpx
from loguru import logger
from prometheus_client import Counter, Histogram

from app.api.dependencies import get_current_user
from app.utils.opa_validator import validate_via_opa
from app.core.settings import settings
from app.core.exceptions import OPAValidationError

GATEWAY_COUNT = Counter("gateway_requests_total", "Total de requisições no gateway", ["status"])
GATEWAY_LATENCY = Histogram("gateway_latency_seconds", "Latência do gateway", ["status"])

router = APIRouter(
    prefix="/gateway",
    tags=["Gateway"],
    responses={
        200: {"description": "Encaminhamento bem-sucedido"},
        403: {"description": "Negado por política OPA"},
        502: {"description": "Erro no serviço downstream"},
        503: {"description": "OPA indisponível"},
    },
)

@router.post("/", response_model=Dict[str, Any], summary="Proxy seguro para LLM e serviços downstream")
async def gateway_forward(
    payload: Dict[str, Any],
    request: Request,
    user=Depends(get_current_user)
) -> Dict[str, Any]:
    GATEWAY_COUNT.labels(status="start").inc()
    with GATEWAY_LATENCY.labels(status="start").time():
        if settings.OPA_ENABLED:
            try:
                allowed = await validate_via_opa({"user": user.email, "action": "gateway"})
            except OPAValidationError as exc:
                logger.error("OPA indisponível: %s", exc)
                raise HTTPException(status_code=503, detail="OPA unavailable")
            if not allowed:
                logger.info("Acesso negado por política OPA | user=%s", user.email)
                raise HTTPException(status_code=403, detail="Gateway denied by policy")

        url = settings.LLM_PROVIDER
        if not url:
            raise HTTPException(status_code=500, detail="LLM provider não configurado")

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                GATEWAY_COUNT.labels(status="success").inc()
                return response.json()

        except httpx.HTTPError as exc:
            logger.error("Erro downstream: %s", exc)
            GATEWAY_COUNT.labels(status="failure").inc()
            raise HTTPException(status_code=502, detail="Downstream service error")