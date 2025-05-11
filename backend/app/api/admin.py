from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from datetime import datetime, timedelta

from loguru import logger
from prometheus_client import Counter

from app.api.dependencies import get_current_user
from app.schemas.user import UserOut
from app.core.db import mongo_connector

ADMIN_COUNT = Counter("admin_requests_total", "Total de requisições administrativas", ["route"])

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={
        200: {"description": "Admin OK ou Estatísticas"},
        403: {"description": "Acesso restrito"}
    }
)

@router.get(
    "/status",
    response_model=Dict[str, str],
    summary="Status do admin endpoint"
)
async def admin_status(user=Depends(get_current_user)) -> Dict[str, str]:
    """
    Status simples de saúde do admin. Apenas emails @admin.com.
    - Gera logs detalhados de acesso.

    Exemplos de resposta:
    - 200: {"status": "admin OK", "time": "<timestamp>"}
    - 403: {"detail": "Admin access required"}
    """
    ADMIN_COUNT.labels(route="/status").inc()
    if not user.email.endswith("@admin.com"):
        logger.warning("admin.status | denied | email=%s", user.email)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    logger.info("admin.status | granted | email=%s", user.email)
    return {"status": "admin OK", "time": datetime.utcnow().isoformat()}

@router.get(
    "/stats",
    response_model=Dict[str, int],
    summary="Estatísticas gerais de uso"
)
async def admin_stats(
    days: int = 1,
    user=Depends(get_current_user)
) -> Dict[str, int]:
    """
    Estatísticas de uso geral:
    - usuários totais
    - logs últimos `days` dias
    - Apenas para admin

    Exemplos de resposta:
    - 200: {"total_users": 10, "recent_logs": 3}
    - 403: {"detail": "Admin access required"}
    """
    ADMIN_COUNT.labels(route="/stats").inc()
    if not user.email.endswith("@admin.com"):
        logger.warning("admin.stats | denied | email=%s", user.email)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    db = await mongo_connector.get_database()
    total_users = await db.users.count_documents({})
    since = datetime.utcnow() - timedelta(days=days)
    recent_logs = await db.log_events.count_documents({"timestamp": {"$gte": since}})

    logger.info("admin.stats | email=%s | users=%d | logs=%d | days=%d", user.email, total_users, recent_logs, days)
    return {"total_users": total_users, "recent_logs": recent_logs}