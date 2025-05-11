#!/usr/bin/env python3
# scripts/create_indexes.py

"""
Cria índices no MongoDB para otimização e TTL:
 - users.email: índice único
 - log_events.timestamp: expira após 30 dias
"""

import asyncio
from loguru import logger

from app.core.db import mongo_connector


async def create_indexes() -> None:
    db = await mongo_connector.get_database()

    logger.info("🔍 Criando índice único em users.email")
    await db.users.create_index("email", unique=True)

    logger.info("🔍 Criando TTL index em log_events.timestamp (30 dias)")
    await db.log_events.create_index("timestamp", expireAfterSeconds=30 * 24 * 3600)

    logger.success("✅ Índices criados com sucesso")


if __name__ == "__main__":
    logger.info("▶️ Iniciando criação de índices...")
    asyncio.run(create_indexes())