from fastapi import APIRouter
from typing import Dict
from loguru import logger
from datetime import datetime

from app.core.db import mongo_connector
from app.core.settings import settings

router = APIRouter(
    tags=["Health"],
    responses={
        200: {"description": "Status OK"},
        500: {"description": "Erro de banco de dados"}
    }
)

@router.get(
    "/health",
    response_model=Dict[str, str],
    summary="Health check do backend"
)
async def health_check() -> Dict[str, str]:
    """
    Health check geral:
    - Verifica conexão MongoDB
    - Retorna status, versão e timestamp UTC
    - Loga falhas de banco

    Exemplos de resposta:
    - 200: {"status": "ok", "version": "1.0.0", "timestamp": "<iso8601>"}
    - 500: {"status": "error", ...}
    """
    try:
        db = await mongo_connector.get_database()
        await db.command("ping")
        status_txt = "ok"
    except Exception as exc:
        logger.error("health_check | mongo connection failed | exc=%s", exc)
        status_txt = "error"

    info = {
        "status": status_txt,
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }
    return info