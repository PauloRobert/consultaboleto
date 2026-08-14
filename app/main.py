from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from app.api.routes.clientes import router as clientes_router
from app.api.routes.pagamentos import router as pagamentos_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, new_request_id
from app.schemas.responses import HealthResponse

settings = get_settings()
configure_logging(settings.log_level, settings.log_json)
logger = logging.getLogger(__name__)
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para consulta de faturas telefônicas.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.middleware("http")
async def security_and_request_id(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    request.state.request_id = request.headers.get("X-Request-ID", new_request_id())[:64]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.get("/health", response_model=HealthResponse, tags=["Sistema"], summary="Verifica a saúde da API")
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=settings.app_version)


app.include_router(clientes_router, prefix="/api/v1")
app.include_router(pagamentos_router, prefix="/api/v1")
register_exception_handlers(app)
