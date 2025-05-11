import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from aioredis import Redis, from_url
from loguru import logger

from app.core.settings import settings
from app.core.exceptions import TokenValidationError

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
_redis: Optional[Redis] = None


async def get_redis() -> Redis:
    """
    Inicializa ou retorna instância única de Redis.
    """
    global _redis
    if _redis is None:
        _redis = await from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )
        logger.info("🔗 Redis conectado em %s", settings.REDIS_URL)
    return _redis


def hash_password(password: str) -> str:
    """Gera hash bcrypt para a senha."""
    return pwd_ctx.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica senha plain vs hashed."""
    return pwd_ctx.verify(plain, hashed)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Cria JWT de acesso com expiração."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "scope": "access_token"})
    token = jwt.encode(
        to_encode, settings.JWT_SECRET.get_secret_value(), algorithm=settings.JWT_ALGORITHM
    )
    return token


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Cria JWT de refresh e armazena-o em Redis para permitir revogação antecipada.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    token = jwt.encode(
        to_encode, settings.JWT_SECRET.get_secret_value(), algorithm=settings.JWT_ALGORITHM
    )
    # Armazena no Redis com TTL
    async def _store():
        redis = await get_redis()
        ttl = int((expire - datetime.utcnow()).total_seconds())
        await redis.setex(f"refresh:{token}", ttl, "1")

    import asyncio

    asyncio.create_task(_store())
    return token


async def is_refresh_token_valid(token: str) -> bool:
    """Verifica se o refresh token existe e ainda é válido."""
    redis = await get_redis()
    return await redis.exists(f"refresh:{token}") == 1


async def revoke_refresh_token(token: str) -> None:
    """Revoga (deleta) o refresh token do Redis."""
    redis = await get_redis()
    await redis.delete(f"refresh:{token}")
    logger.info("Refresh token revogado")


def decode_token(token: str, expected_scope: str) -> Dict[str, Any]:
    """
    Decodifica e valida JWT.
    Garante escopo (access_token vs refresh_token) e expiração.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as exc:
        logger.error("⚠ JWT decode error: %s", exc)
        raise TokenValidationError("Token inválido ou expirado") from exc

    scope = payload.get("scope")
    if scope != expected_scope:
        raise TokenValidationError(f"Escopo inválido: {scope}")

    return payload