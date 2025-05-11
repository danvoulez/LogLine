import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.settings import settings
from app.core.db import mongo_connector
from app.core.exceptions import (
    CredentialsException,
    TokenValidationError,
    OPAValidationError
)

# Import de todos os routers organizados por funcionalidade
from app.api.auth     import router as auth_router
from app.api.actions  import router as actions_router
from app.api.query    import router as query_router
from app.api.timeline import router as timeline_router
from app.api.users    import router as users_router
from app.api.webhooks import router as webhooks_router
from app.api.gateway  import router as gateway_router
from app.api.admin    import router as admin_router
from app.api.health   import router as health_router


def create_app() -> FastAPI:
    """
    Configura e retorna a instância FastAPI pronta para rodar,
    com middlewares, handlers globais e todos os routers registrados.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_prefix=settings.API_V1_PREFIX,
    )

    # — Middleware CORS —
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # — Exception Handlers Globais —

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("🛑 Request inválida %s: %s", request.url, exc.errors())
        return JSONResponse(
            status_code=422,
            content={"error": "invalid_request", "details": exc.errors()},
        )

    @app.exception_handler(CredentialsException)
    async def credentials_exception_handler(request: Request, exc: CredentialsException):
        logger.warning("🔒 Auth falhou %s: %s", request.url, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "authentication_failed", "message": exc.detail},
        )

    @app.exception_handler(TokenValidationError)
    async def token_exception_handler(request: Request, exc: TokenValidationError):
        logger.warning("🔐 Token inválido %s: %s", request.url, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "token_invalid", "message": exc.detail},
        )

    @app.exception_handler(OPAValidationError)
    async def opa_exception_handler(request: Request, exc: OPAValidationError):
        if not settings.OPA_ENABLED:
            # Fallback seguro quando OPA estiver desativado
            logger.warning("⚙️ OPA desativado, liberando ação %s", request.url)
            return JSONResponse(status_code=200, content={"status": "opa_disabled"})
        logger.error("🛑 OPA falhou %s: %s", request.url, str(exc))
        return JSONResponse(
            status_code=503,
            content={"error": "opa_error", "message": str(exc)},
        )

    # — Eventos de Ciclo de Vida —

    @app.on_event("startup")
    async def on_startup():
        # Configura logger
        logger.info("🚀 Iniciando aplicação %s v%s", settings.PROJECT_NAME, settings.VERSION)
        # Conecta ao MongoDB
        await mongo_connector.connect()
        logger.success("✅ Startup completo")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("🔌 Encerrando aplicação...")
        await mongo_connector.close()
        logger.success("🧨 Shutdown completo")

    # — Registro de Routers —
    for router in (
        auth_router,
        actions_router,
        query_router,
        timeline_router,
        users_router,
        webhooks_router,
        gateway_router,
        admin_router,
        health_router,
    ):
        app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.core.main:app",
        host="0.0.0.0",
        port=10000,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.RELOAD,
    )