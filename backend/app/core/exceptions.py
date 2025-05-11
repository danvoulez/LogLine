from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse

class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Não foi possível validar credenciais"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ValidationException(HTTPException):
    def __init__(self, detail: str = "Dados de entrada inválidos"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )

class InternalError(HTTPException):
    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

# Handler genérico para qualquer HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.detail
        },
        headers=getattr(exc, "headers", None)
    )