from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.api.v1.router import api_v1_router
from backend.app.core.config import settings
from backend.app.core.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from backend.app.core.logging import setup_logging
from backend.app.database.connection import engine

logger = logging.getLogger("script_scrapper.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Lifespan
    setup_logging(level="INFO")
    logger.info("Initializing Script Scrapper Backend API...")
    logger.info(f"Environment: {settings.ENVIRONMENT} | API Prefix: {settings.API_V1_STR}")
    logger.info(f"Database Pool Size: {settings.DB_POOL_SIZE} (Max Overflow: {settings.DB_MAX_OVERFLOW})")
    
    yield
    
    # Shutdown Lifespan
    logger.info("Shutting down Script Scrapper Backend API...")
    await engine.dispose()
    logger.info("Database connection engine disposed cleanly.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Exception Handlers Registration
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API v1 Router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "success": True,
        "data": {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "api_v1": settings.API_V1_STR,
            "docs": f"{settings.API_V1_STR}/docs",
            "health": f"{settings.API_V1_STR}/health",
            "system_status": f"{settings.API_V1_STR}/system/status",
        },
    }
