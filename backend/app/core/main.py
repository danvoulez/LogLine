import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.settings import settings
from app.core.db import mongo_connector
from app.core.exceptions import (
    CredentialsException,
    ValidationException,
    InternalError,
    http_exception_handler
)

from app.api.auth     import router as auth_router
from app.api.actions  import router as actions_router
from app.api.query    import router as query_router
from app.api.timeline import router as timeline_router
from app.api.users    import router as users_router
from app.api.webhooks import router as webhooks_router
from app.api.gateway  import router as gateway_router
from app.api.admin    import router as admin_router
from app.api.health   import router as health_router

def configure_logging():
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=settings.LOG_LEVEL.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        root_path="",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    @app.get("/", include_in_schema=False)
    async def root():
        return {"status": "ok", "version": settings.VERSION}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Request inválida: {request.method} {request.url}")
        return JSONResponse(
            status_code=422,
            content={"error": "invalid_request", "details": exc.errors()}
        )

    app.add_exception_handler(HTTPException, http_exception_handler)

    @app.on_event("startup")
    async def on_startup():
        logger.info(f"🚀 Iniciando {settings.PROJECT_NAME} v{settings.VERSION}")
        await mongo_connector.connect()

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("🛑 Encerrando aplicação")
        await mongo_connector.close()

    for r in (
        auth_router, actions_router, query_router, timeline_router,
        users_router, webhooks_router, gateway_router, admin_router, health_router
    ):
        app.include_router(r)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.core.main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.RELOAD
    )