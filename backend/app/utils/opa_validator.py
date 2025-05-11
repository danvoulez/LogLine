from typing import Any, Dict
import httpx
from loguru import logger

from app.core.settings import settings
from app.core.exceptions import OPAValidationError

async def validate_via_opa(input_data: Dict[str, Any], policy_path: str = "myapp/policy/allow") -> bool:
    """
    Consulta o OPA para verificar se uma ação é permitida.
    - Se OPA estiver desabilitado, permite automaticamente.
    - Se OPA falhar com rede, registra e decide com fallback.
    """
    if not settings.OPA_ENABLED:
        logger.debug("OPA desativado — liberando por padrão.")
        return True

    if not settings.OPA_URL:
        raise OPAValidationError("OPA_URL não configurado")

    endpoint = f"{settings.OPA_URL}/v1/data/{policy_path}"
    timeout = httpx.Timeout(connect=1.0, read=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(endpoint, json={"input": input_data})
            resp.raise_for_status()
            result = resp.json().get("result", {})
            allow = result.get("allow", False)
            logger.debug("OPA response allow=%s | input=%s", allow, input_data)
            return bool(allow)

    except httpx.RequestError as exc:
        logger.warning("OPA erro de rede: %s", exc)
        if settings.OPA_ENABLED:
            raise OPAValidationError(str(exc)) from exc
        return True