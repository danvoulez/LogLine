#!/usr/bin/env python3
# scripts/seed_data.py

"""
Popula o banco com usuários e logs de exemplo para dev/testing.
"""

import asyncio
import random
from datetime import datetime, timedelta

from loguru import logger

from app.core.db import mongo_connector
from app.utils.security import hash_password


async def seed_users() -> None:
    db = await mongo_connector.get_database()
    users = [
        {"email": "alice@corp.com", "password": "Alice1234!"},
        {"email": "bob@corp.com", "password": "Bob12345!"},
        {"email": "charlie@corp.com", "password": "Charlie123!"},
    ]

    for u in users:
        if await db.users.find_one({"email": u["email"]}):
            logger.warning("Usuário já existe: %s", u["email"])
            continue

        doc = {
            "email": u["email"],
            "hashed_password": hash_password(u["password"]),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
        }
        await db.users.insert_one(doc)
        logger.success("Usuário criado: %s", u["email"])


async def seed_logs(n: int = 100) -> None:
    db = await mongo_connector.get_database()
    user_ids = [str(u["_id"]) for u in await db.users.find({}, {"_id": 1}).to_list(None)]
    if not user_ids:
        logger.error("Nenhum usuário disponível para seed de logs")
        return

    now = datetime.utcnow()
    for i in range(n):
        doc = {
            "user_id": random.choice(user_ids),
            "action": random.choice(["login", "create_order", "update_profile"]),
            "details": {"info": f"seed_{i}"},
            "timestamp": now - timedelta(minutes=random.randint(0, 1440)),
        }
        await db.log_events.insert_one(doc)

    logger.success("✓ Seed de %d logs inseridos", n)


async def main() -> None:
    logger.info("▶️ Iniciando seed de dados...")
    await seed_users()
    await seed_logs(100)
    logger.success("✅ Seed completo")


if __name__ == "__main__":
    asyncio.run(main())