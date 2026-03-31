from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import register_exception_handlers
from app.domains.company.router import router as company_router
from app.domains.dashboard.router import router as dashboard_router
from app.domains.news.router import router as news_router
from app.domains.product.router import router as product_router
from app.domains.spec_change.router import router as spec_change_router
from app.domains.spec_field.router import router as spec_field_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="BARO API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(company_router, prefix="/api")
    app.include_router(product_router, prefix="/api")
    app.include_router(spec_field_router, prefix="/api")
    app.include_router(news_router, prefix="/api")
    app.include_router(spec_change_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")

    return app


app = create_app()
