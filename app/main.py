from fastapi import FastAPI, Request

from app.core.config import settings
from app.utils.error import AppBaseError
from app.api.auth import router


app = FastAPI(
    name="coffee-auth-service",
    description="Сервис аутентификации"
)


@app.exception_handler(AppBaseError)
async def shortener_base_error_handler(
        request: Request,
        exc: AppBaseError
):
    raise exc.http()


app.include_router(router, prefix=settings.api.prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
