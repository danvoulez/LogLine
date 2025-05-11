import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger

from app.core.settings import settings


class MongoConnector:
    """
    Gerencia a conexão com MongoDB, garantindo:
     - instanciação única (singleton)
     - retry com backoff exponencial
     - healthcheck no startup
     - desconexão limpa no shutdown
    """

    _client: Optional[AsyncIOMotorClient] = None
    _lock = asyncio.Lock()

    async def connect(self) -> AsyncIOMotorClient:
        """
        Estabelece conexão com o MongoDB.
        Tenta até 3 vezes com backoff exponencial antes de falhar.
        """
        async with self._lock:
            if self._client is None:
                retries = 3
                base_delay = 1.0
                for attempt in range(1, retries + 1):
                    try:
                        logger.info(f"🔗 Conectando ao MongoDB (tentativa {attempt}/{retries})...")
                        client = AsyncIOMotorClient(
                            settings.MONGO_URL,
                            serverSelectionTimeoutMS=5000,
                            uuidRepresentation='standard'
                        )
                        await client.admin.command("ping")
                        logger.success("✅ MongoDB conectado com sucesso")
                        self._client = client
                        break
                    except Exception as exc:
                        logger.warning(f"❌ Falha de conexão (attempt {attempt}): {exc}")
                        if attempt == retries:
                            logger.error("🛑 Todas as tentativas falharam. Abortando.")
                            raise
                        await asyncio.sleep(base_delay * attempt)
            return self._client

    async def get_database(self) -> AsyncIOMotorDatabase:
        """
        Retorna instância de AsyncIOMotorDatabase.
        """
        client = await self.connect()
        # Se houver nome de DB no URL, esse será usado; senão, default_database
        return client.get_default_database()

    async def close(self) -> None:
        """
        Fecha a conexão com o MongoDB (usado no shutdown do app).
        """
        if self._client:
            logger.info("🔌 Fechando conexão com MongoDB...")
            self._client.close()
            self._client = None


# Exporta a instância para uso global
mongo_connector = MongoConnector()